import json
import os
from io import StringIO
from unittest.mock import Mock, patch

from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from . import utils
from .ai_descriptions import generate_description
from .models import Product, Comment, Order, OrderItem, Review, PriceHistory, UserAddress, Wallet


class ProductModelTests(TestCase):
    def test_str_returns_product_name(self):
        p = Product.objects.create(name='Test Product', price=10.0, stock=5, image_url='http://a.png')
        self.assertEqual(str(p), 'Test Product')

    def test_additional_images_property_honors_optional_urls(self):
        p = Product.objects.create(name='Test', price=1.0, stock=1, image_url='http://a.png', image_2='http://b.png')
        self.assertEqual(p.additional_images, ['http://b.png'])

    def test_price_history_is_recorded_when_price_changes(self):
        p = Product.objects.create(name='Pricey', price=10.0, stock=2, image_url='http://a.png')
        self.assertTrue(PriceHistory.objects.filter(product=p, price=10.0).exists())

        p.price = 12.5
        p.save()

        history = PriceHistory.objects.filter(product=p).order_by('recorded_at', 'id')
        self.assertEqual(history.count(), 2)
        self.assertEqual(history.first().price, 10.0)
        self.assertEqual(history.last().price, 12.5)


class GuestCartAccessTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Widget', price=20.0, stock=10, image_url='http://a.png')

    def test_guest_is_sent_to_login_and_nothing_is_added(self):
        add_url = reverse('products:add-to-cart', args=[self.product.id])
        response = self.client.get(add_url)
        self.assertRedirects(response, f"{reverse('products:login')}?next={add_url}", fetch_redirect_response=False)
        self.assertNotIn('cart', self.client.session)

    def test_guest_cannot_open_cart_checkout_or_buy_now(self):
        for url in [
            reverse('products:view-cart'),
            reverse('products:checkout'),
            reverse('products:buy-now', args=[self.product.id]),
        ]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response['Location'].startswith(reverse('products:login')))

    def test_guest_ajax_cart_update_gets_401_json(self):
        response = self.client.post(
            reverse('products:update-cart'), data='{}', content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['login_url'], reverse('products:login'))

    def test_login_completes_pending_add_to_cart(self):
        User.objects.create_user(username='shopper', password='pass12345')
        add_url = reverse('products:add-to-cart', args=[self.product.id])
        response = self.client.post(
            f"{reverse('products:login')}?next={add_url}",
            {'username_or_email': 'shopper', 'password': 'pass12345'},
            follow=True,
        )
        self.assertEqual(self.client.session['cart'], {str(self.product.id): 1})
        self.assertEqual(response.status_code, 200)

    def test_login_ignores_offsite_next_url(self):
        User.objects.create_user(username='shopper', password='pass12345')
        response = self.client.post(
            f"{reverse('products:login')}?next=https://evil.example.com/",
            {'username_or_email': 'shopper', 'password': 'pass12345'},
        )
        self.assertEqual(response['Location'], reverse('products:product-list'))


class CartViewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Widget', price=20.0, stock=10, image_url='http://a.png')
        User.objects.create_user(username='cart-user', password='pass')
        self.client.login(username='cart-user', password='pass')

    def test_add_to_cart_sets_session(self):
        response = self.client.post(reverse('products:add-to-cart', args=[self.product.id]), follow=True)
        self.assertEqual(self.client.session['cart'], {str(self.product.id): 1})
        self.assertEqual(response.status_code, 200)

    def test_view_cart_shows_item_and_total(self):
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()

        response = self.client.get(reverse('products:view-cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Widget')
        self.assertContains(response, '40.0')

    def test_delete_from_cart_removes_item(self):
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()

        response = self.client.post(reverse('products:delete-from-cart', args=[self.product.id]), follow=True)
        self.assertEqual(self.client.session['cart'], {})

    def test_checkout_computes_total_kobo_and_context(self):
        session = self.client.session
        session['cart'] = {str(self.product.id): 3}
        session.save()

        response = self.client.get(reverse('products:checkout'))
        self.assertEqual(response.context['total'], 60.0)
        self.assertEqual(response.context['total_kobo'], 6000)

    def test_checkout_exposes_paystack_callback_context(self):
        user = User.objects.create_user(username='checkout-user', password='pass')
        self.client.login(username='checkout-user', password='pass')

        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()

        response = self.client.get(reverse('products:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('paystack_public_key', response.context)
        self.assertIn('paystack_callback_url', response.context)
        self.assertTrue(str(response.context['paystack_callback_url']).endswith('/payments/callback/'))

    def test_checkout_renders_add_address_link_when_user_has_no_saved_addresses(self):
        user = User.objects.create_user(username='checkout-address-user', password='pass', email='address@example.com')
        self.client.login(username='checkout-address-user', password='pass')

        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()

        response = self.client.get(reverse('products:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="shipping-address"')
        self.assertContains(response, 'Add a new address')
        self.assertContains(response, reverse('products:add-address'))

    def test_test_email_route_is_removed(self):
        response = self.client.get('/products/test-email/')
        self.assertEqual(response.status_code, 404)

    def test_account_dashboard_is_available_for_authenticated_user(self):
        user = User.objects.create_user(username='account-user', password='pass', email='account@example.com')
        self.client.login(username='account-user', password='pass')

        response = self.client.get(reverse('account-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Account')
        self.assertContains(response, 'Wallet')
        self.assertContains(response, 'Order History')

    def test_buy_now_sets_cart_directly(self):
        response = self.client.get(reverse('products:buy-now', args=[self.product.id]), follow=True)
        self.assertEqual(self.client.session['cart'], {str(self.product.id): 1})

    def test_confirm_payment_clears_cart(self):
        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()

        response = self.client.post(reverse('products:confirm-payment'), follow=True)
        self.assertEqual(self.client.session['cart'], {})

    def test_confirm_payment_returns_order_success_redirect_for_cod(self):
        user = User.objects.create_user(username='cod-user', password='pass', email='cod@example.com')
        self.client.login(username='cod-user', password='pass')

        address = UserAddress.objects.create(
            user=user,
            full_name='Cod User',
            phone='08000000000',
            street_address='1 Test Street',
            city='Lagos',
            state='Lagos',
            postal_code='100001'
        )

        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()

        response = self.client.post(
            reverse('products:confirm-payment'),
            data=json.dumps({
                'payment_channel': 'cod',
                'shipping_address_id': address.id,
                'insurance_opted': 'false',
                'insurance_cost': '0',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('/products/order-success/', data['redirect'])
        self.assertIn('order_id', data)


class ProductDetailTests(TestCase):
    def setUp(self):
        cache.clear()
        self.product = Product.objects.create(name='Gadget', price=15.0, stock=7, image_url='http://a.png')

    def test_product_detail_page_get(self):
        response = self.client.get(reverse('products:product-detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gadget')

    def test_product_detail_uses_fallback_for_blank_description(self):
        response = self.client.get(reverse('products:product-detail', args=[self.product.id]))

        self.assertContains(response, 'No description available yet.')

    def test_product_detail_generates_and_saves_ai_description_when_descriptions_are_blank(self):
        Product.objects.filter(pk=self.product.pk).update(description='')
        with patch('products.views.generate_description', return_value='A useful gadget for everyday tasks. It is listed in the Other category.') as generate:
            response = self.client.get(reverse('products:product-detail', args=[self.product.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A useful gadget for everyday tasks.')
        self.product.refresh_from_db()
        self.assertEqual(self.product.ai_description, 'A useful gadget for everyday tasks. It is listed in the Other category.')
        generate.assert_called_once()

    def test_product_detail_caches_generation_failures(self):
        Product.objects.filter(pk=self.product.pk).update(description='')
        with patch('products.views.generate_description', return_value=None) as generate:
            first_response = self.client.get(reverse('products:product-detail', args=[self.product.id]))
            second_response = self.client.get(reverse('products:product-detail', args=[self.product.id]))

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertContains(second_response, 'No description available yet.')
        self.assertTrue(cache.get(f'groq_fail:{self.product.pk}'))
        generate.assert_called_once()

    def test_product_detail_prefers_curated_description_over_ai_description(self):
        Product.objects.filter(pk=self.product.pk).update(
            description='Regular product description.',
            ai_description='AI product description.',
        )
        with patch('products.views.generate_description') as generate:
            response = self.client.get(reverse('products:product-detail', args=[self.product.id]))

        self.assertContains(response, 'Regular product description.')
        self.assertNotContains(response, 'AI product description.')
        generate.assert_not_called()

    def test_product_detail_does_not_generate_when_regular_description_exists(self):
        Product.objects.filter(pk=self.product.pk).update(description='Regular product description.')
        with patch('products.views.generate_description') as generate:
            response = self.client.get(reverse('products:product-detail', args=[self.product.id]))

        self.assertContains(response, 'Regular product description.')
        generate.assert_not_called()

    def test_product_detail_post_comment(self):
        response = self.client.post(reverse('products:product-detail', args=[self.product.id]), {
            'name': 'Alice',
            'text': 'Nice!',
            'rating': '4'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(product=self.product, name='Alice', rating=4).exists())

    def test_review_submission_marks_verified_purchase(self):
        user = User.objects.create_user(username='reviewer', password='pass')
        self.client.login(username='reviewer', password='pass')
        order = Order.objects.create(user=user, status='delivered', payment_status='paid', is_paid=True)
        OrderItem.objects.create(order=order, product=self.product, quantity=1, price=self.product.price)

        response = self.client.post(reverse('products:submit-review', args=[self.product.id]), {
            'rating': '5',
            'review_text': 'Excellent product'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        review = Review.objects.get(product=self.product, user=user)
        self.assertEqual(review.rating, 5)
        self.assertTrue(review.verified_purchase)


class ProductDescriptionGenerationTests(TestCase):
    def test_generate_description_uses_groq_timeout_and_returns_two_sentences(self):
        result = 'A practical item for everyday use. This listing is categorized under Home.'
        with patch('products.utils._get_groq_api_key', return_value='test-key'), patch(
            'products.utils._call_groq',
            return_value=result,
        ) as call_groq:
            description = generate_description(Product(
                name='Kitchen Item',
                category='Home',
                price=12.5,
            ))

        self.assertEqual(description, result)
        call_groq.assert_called_once()
        self.assertEqual(call_groq.call_args.kwargs['timeout'], 10)
        self.assertEqual(call_groq.call_args.kwargs['retries'], 1)

    def test_generate_description_rejects_invalid_sentence_count(self):
        with patch('products.utils._get_groq_api_key', return_value='test-key'), patch(
            'products.utils._call_groq',
            return_value='Only one sentence.',
        ) as call_groq:
            description = generate_description(Product(name='Kitchen Item', category='Home', price=12.5))

        self.assertIsNone(description)
        call_groq.assert_called_once()

    def test_new_empty_product_description_is_filled_by_post_save_signal(self):
        with patch('products.ai_descriptions.generate_description', return_value='A useful product. Suitable for everyday use.') as generate:
            product = Product.objects.create(
                name='New Product',
                price=10.0,
                stock=1,
                image_url='http://a.png',
                description='',
            )

        product.refresh_from_db()
        self.assertEqual(product.description, 'A useful product. Suitable for everyday use.')
        generate.assert_called_once()


class GroqClientTests(TestCase):
    def test_call_groq_uses_configured_model_and_ten_second_timeout(self):
        response = Mock()
        response.json.return_value = {
            'choices': [{'message': {'content': 'Generated response.'}}],
        }

        with patch('products.utils._get_groq_api_key', return_value='test-key'), patch(
            'products.utils.settings.GROQ_MODEL', 'openai/gpt-oss-120b',
        ), patch('products.utils.requests.post', return_value=response) as post:
            result = utils._call_groq(prompt='Test prompt')

        self.assertEqual(result, 'Generated response.')
        self.assertEqual(post.call_args.kwargs['json']['model'], 'openai/gpt-oss-120b')
        self.assertEqual(post.call_args.kwargs['timeout'], 10)

    def test_call_groq_does_not_call_api_without_model(self):
        with patch('products.utils._get_groq_api_key', return_value='test-key'), patch(
            'products.utils.settings.GROQ_MODEL', '',
        ), patch('products.utils.requests.post') as post:
            result = utils._call_groq(prompt='Test prompt')

        self.assertIsNone(result)
        post.assert_not_called()

    def test_call_groq_handles_request_exception_without_retrying(self):
        with patch('products.utils._get_groq_api_key', return_value='test-key'), patch(
            'products.utils.settings.GROQ_MODEL', 'openai/gpt-oss-120b',
        ), patch(
            'products.utils.requests.post',
            side_effect=utils.requests.exceptions.ConnectionError('unavailable'),
        ) as post:
            result = utils._call_groq(prompt='Test prompt', retries=5)

        self.assertIsNone(result)
        post.assert_called_once()


class EnsureSuperuserCommandTests(TestCase):
    def test_missing_environment_values_warn_and_exit_cleanly(self):
        output = StringIO()
        with patch.dict(os.environ, {
            'DJANGO_SUPERUSER_USERNAME': '',
            'DJANGO_SUPERUSER_EMAIL': '',
            'DJANGO_SUPERUSER_PASSWORD': '',
        }):
            call_command('ensure_superuser', stdout=output)

        self.assertIn('Skipping superuser setup', output.getvalue())

    def test_command_creates_then_repairs_superuser_without_printing_password(self):
        environment = {
            'DJANGO_SUPERUSER_USERNAME': 'deploy-admin',
            'DJANGO_SUPERUSER_EMAIL': 'deploy-admin@example.com',
            'DJANGO_SUPERUSER_PASSWORD': 'Test-Only-Password-123!',
        }
        output = StringIO()
        with patch.dict(os.environ, environment):
            call_command('ensure_superuser', stdout=output)
            user = User.objects.get(username='deploy-admin')
            user.is_staff = False
            user.is_superuser = False
            user.is_active = False
            user.set_password('old-password')
            user.save()
            call_command('ensure_superuser', stdout=output)

        user.refresh_from_db()
        self.assertTrue(user.check_password(environment['DJANGO_SUPERUSER_PASSWORD']))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(User.objects.filter(username='deploy-admin').count(), 1)
        self.assertNotIn(environment['DJANGO_SUPERUSER_PASSWORD'], output.getvalue())


class ShopFilterTests(TestCase):
    def setUp(self):
        self.alpha = Product.objects.create(name='Alpha Phone', price=100.0, stock=5, category='Electronics', image_url='http://a.png')
        self.beta = Product.objects.create(name='Beta Phone', price=300.0, stock=5, category='Electronics', image_url='http://b.png')
        self.camera = Product.objects.create(name='Alpha Camera', price=200.0, stock=5, category='Accessories', image_url='http://c.png')

    def test_filters_combine_with_search_and_preserve_query_values(self):
        response = self.client.get(reverse('products:product-list'), {
            'search': 'Alpha',
            'category': 'Electronics',
            'min_price': '50',
            'max_price': '150',
            'sort': 'low-high',
        })

        products = response.context['products']
        self.assertEqual([product.id for product in products], [self.alpha.id])
        self.assertEqual(response.context['query'], 'Alpha')
        self.assertEqual(response.context['selected_category'], 'Electronics')
        self.assertEqual(response.context['min_price'], '50')
        self.assertEqual(response.context['max_price'], '150')
        self.assertEqual(response.context['selected_sort'], 'low-high')

    def test_supported_sort_modes_order_results(self):
        expected_orders = {
            'low-high': [self.alpha.id, self.camera.id, self.beta.id],
            'high-low': [self.beta.id, self.camera.id, self.alpha.id],
            'newest': [self.camera.id, self.beta.id, self.alpha.id],
            'name': [self.camera.id, self.alpha.id, self.beta.id],
        }

        for sort, expected_ids in expected_orders.items():
            with self.subTest(sort=sort):
                response = self.client.get(reverse('products:product-list'), {'sort': sort})
                self.assertEqual([product.id for product in response.context['products']], expected_ids)

    def test_search_matches_description_and_paginates(self):
        Product.objects.filter(pk=self.camera.pk).update(description='Mirrorless body with a zoom lens.')
        response = self.client.get(reverse('products:product-list'), {'search': 'mirrorless'})
        self.assertEqual([product.id for product in response.context['products']], [self.camera.id])

        for index in range(30):
            Product.objects.create(name=f'Bulk {index}', price=10.0, stock=1, category='Other', image_url='http://x.png')
        first = self.client.get(reverse('products:product-list'))
        second = self.client.get(reverse('products:product-list'), {'page': 2})
        self.assertEqual(len(first.context['products']), 24)
        self.assertEqual(len(second.context['products']), 9)
        self.assertContains(second, 'Page 2 of 2')

    def test_unknown_category_is_ignored(self):
        response = self.client.get(reverse('products:product-list'), {'category': 'Nope'})
        self.assertEqual(response.context['selected_category'], '')
        self.assertEqual(len(response.context['products']), 3)


class OrderTrackingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tracker', password='pass')
        self.client.login(username='tracker', password='pass')
        self.order = Order.objects.create(user=self.user, status='processing', tracking_number='TRK123')

    def test_order_tracking_page_renders_status_steps(self):
        response = self.client.get(reverse('products:order-track', args=[self.order.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Placed')
        self.assertContains(response, 'Processing')
        self.assertContains(response, 'Shipped')
        self.assertContains(response, 'Delivered')
        self.assertContains(response, 'TRK123')


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='pass')
        self.product = Product.objects.create(name='Item', price=10.0, stock=5, image_url='http://a.png')
        self.order = Order.objects.create(user=self.user)

    def test_order_total_and_orderitem_total_price(self):
        OrderItem.objects.create(order=self.order, product=self.product, quantity=3, price=10.0)
        self.assertEqual(self.order.total, 30.0)
        item = self.order.items.first()
        self.assertEqual(item.total_price, 30.0)

    def test_release_escrow_updates_status(self):
        self.order.is_paid = True
        self.order.escrow_status = 'held'
        self.order.save()

        response = self.client.login(username='john', password='pass')
        self.assertTrue(response)

        response = self.client.post(reverse('products:release-escrow', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.escrow_status, 'released')
        self.assertTrue(self.order.escrow_release_date is not None)

    def test_escrow_helpers_reflect_paid_protected_orders(self):
        self.order.is_paid = True
        self.order.escrow_status = 'held'
        self.order.save()

        self.assertTrue(self.order.escrow_is_protected)
        self.assertEqual(self.order.escrow_badge, 'Protected')

    def test_delivered_orders_release_escrow_automatically(self):
        self.order.is_paid = True
        self.order.escrow_status = 'held'
        self.order.status = 'delivered'
        self.order.delivered_date = timezone.now()
        self.order.save()

        self.order.refresh_from_db()
        self.assertEqual(self.order.escrow_status, 'released')
        self.assertIsNotNone(self.order.escrow_release_date)


class ReferralProgramTests(TestCase):
    def setUp(self):
        from . import referrals
        self.referrals = referrals
        self.referrer = User.objects.create_user(username='ada', password='pass12345', first_name='Ada')

    def _signup_via_link(self, username='friend'):
        code = self.referrals.referral_code_for(self.referrer)
        landing = self.client.get(reverse('products:referral', args=[code]))
        self.assertRedirects(landing, reverse('products:register'), fetch_redirect_response=False)
        page = self.client.get(reverse('products:register'))
        self.assertContains(page, 'You were invited by')
        self.client.post(reverse('products:register'), {
            'username': username, 'email': f'{username}@example.com',
            'password': 'longpassword1', 'password_confirm': 'longpassword1',
        })
        return User.objects.get(username=username)

    def test_signup_through_link_records_referral(self):
        friend = self._signup_via_link()
        self.assertEqual(friend.referral_record.referrer, self.referrer)
        self.assertFalse(friend.referral_record.reward_paid)

    def test_first_paid_order_pays_referrer_once(self):
        friend = self._signup_via_link()
        Order.objects.create(user=friend, status='processing', payment_status='unpaid', is_paid=False)
        self.assertFalse(Wallet.objects.filter(user=self.referrer, balance__gt=0).exists())

        Order.objects.create(user=friend, status='processing', payment_status='paid', is_paid=True)
        Order.objects.create(user=friend, status='processing', payment_status='paid', is_paid=True)
        wallet = Wallet.objects.get(user=self.referrer)
        self.assertEqual(wallet.balance, 1000.0)
        self.assertEqual(wallet.transactions.filter(transaction_type='reward').count(), 1)

    def test_tampered_code_is_rejected(self):
        code = self.referrals.referral_code_for(self.referrer)
        forged = code.split('-')[0] + '-deadbeef'
        response = self.client.get(reverse('products:referral', args=[forged]))
        self.assertRedirects(response, reverse('products:register'), fetch_redirect_response=False)
        self.assertNotIn(self.referrals.SESSION_KEY, self.client.session)

    def test_referrals_page_shows_personal_link(self):
        self.client.login(username='ada', password='pass12345')
        response = self.client.get(reverse('products:referrals'))
        self.assertContains(response, self.referrals.referral_code_for(self.referrer))

    def test_cart_invite_button_uses_personal_link(self):
        self.client.login(username='ada', password='pass12345')
        product = Product.objects.create(name='Widget', price=20.0, stock=10, image_url='http://a.png')
        self.client.get(reverse('products:add-to-cart', args=[product.id]))
        response = self.client.get(reverse('products:view-cart'))
        self.assertContains(response, self.referrals.referral_code_for(self.referrer))


class AddressFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='addr', password='pass12345', first_name='Tolu', last_name='Ade')
        self.client.login(username='addr', password='pass12345')
        self.valid = {
            'full_name': 'Tolu Ade', 'phone': '0803 123 4567', 'street_address': '12 Admiralty Way',
            'landmark': 'opposite Shoprite', 'city': 'Lekki', 'state': 'Lagos', 'postal_code': '',
            'address_type': 'home',
        }

    def test_adding_from_checkout_returns_to_checkout_with_address_selected(self):
        checkout = reverse('products:checkout')
        response = self.client.post(f"{reverse('products:add-address')}?next={checkout}", self.valid)
        address = UserAddress.objects.get(user=self.user)
        self.assertRedirects(response, f'{checkout}?address={address.pk}', fetch_redirect_response=False)
        self.assertTrue(address.is_default)  # first address becomes default
        self.assertEqual(address.phone, '08031234567')
        self.assertIn('near opposite Shoprite', address.street_address)

        session = self.client.session
        session['cart'] = {str(Product.objects.create(name='W', price=5.0, stock=3, image_url='http://a.png').pk): 1}
        session.save()
        page = self.client.get(f'{checkout}?address={address.pk}')
        self.assertEqual(page.context['selected_address_id'], address.pk)

    def test_without_next_returns_to_address_book_and_ignores_offsite_next(self):
        response = self.client.post(reverse('products:add-address'), self.valid)
        self.assertRedirects(response, reverse('products:addresses'), fetch_redirect_response=False)
        response = self.client.post(f"{reverse('products:add-address')}?next=https://evil.example.com/", self.valid)
        self.assertRedirects(response, reverse('products:addresses'), fetch_redirect_response=False)

    def test_invalid_form_keeps_values_and_shows_field_errors(self):
        data = dict(self.valid, phone='abc', state='Atlantis')
        response = self.client.post(reverse('products:add-address'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('phone', response.context['errors'])
        self.assertIn('state', response.context['errors'])
        self.assertContains(response, 'value="12 Admiralty Way"')
        self.assertFalse(UserAddress.objects.exists())

    def test_only_one_default_and_deleting_default_promotes_another(self):
        self.client.post(reverse('products:add-address'), self.valid)
        self.client.post(reverse('products:add-address'), dict(self.valid, street_address='5 Allen Avenue', is_default='on'))
        first, second = UserAddress.objects.order_by('created_at', 'id')
        self.assertFalse(first.is_default)
        self.assertTrue(UserAddress.objects.get(pk=second.pk).is_default)

        self.client.post(reverse('products:delete-address', args=[second.pk]))
        self.assertTrue(UserAddress.objects.get(pk=first.pk).is_default)

    def test_set_default_switches_default(self):
        self.client.post(reverse('products:add-address'), self.valid)
        self.client.post(reverse('products:add-address'), dict(self.valid, street_address='5 Allen Avenue'))
        first, second = UserAddress.objects.order_by('created_at', 'id')
        self.client.post(reverse('products:set-default-address', args=[second.pk]))
        self.assertEqual(list(UserAddress.objects.filter(is_default=True).values_list('pk', flat=True)), [second.pk])
