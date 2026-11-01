from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Product, Review


class CatalogApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.phone = Product.objects.create(
            name='Pixel 9', price=900000, stock=5, category='Phones', image_url='https://img.test/p.jpg',
            description='Android phone',
        )
        cls.cheap_phone = Product.objects.create(
            name='Nokia 105', price=20000, stock=0, category='Phones', image_url='https://img.test/n.jpg',
        )
        cls.laptop = Product.objects.create(
            name='ThinkPad X1', price=1500000, stock=10, category='Laptops', image_url='https://img.test/t.jpg',
            sale_price=1200000, sale_ends_at=timezone.now() + timedelta(days=1),
        )
        user = User.objects.create_user('ada', password='x')
        other = User.objects.create_user('bola', password='x')
        Review.objects.create(user=user, product=cls.phone, rating=4, moderation_status='published')
        Review.objects.create(user=other, product=cls.phone, rating=2, moderation_status='hidden')

    def test_list_returns_products_categories_and_paging(self):
        data = self.client.get(reverse('products:api-v1-product-list')).json()
        self.assertEqual(data['count'], 3)
        self.assertEqual(data['page'], 1)
        self.assertEqual({c['value'] for c in data['categories']}, {'Phones', 'Laptops'})

    def test_search_category_and_sort(self):
        url = reverse('products:api-v1-product-list')
        self.assertEqual([p['name'] for p in self.client.get(url, {'q': 'thinkpad'}).json()['results']], ['ThinkPad X1'])
        names = [p['name'] for p in self.client.get(url, {'category': 'Phones', 'sort': 'price_asc'}).json()['results']]
        self.assertEqual(names, ['Nokia 105', 'Pixel 9'])

    def test_unknown_category_and_bad_page_are_ignored_safely(self):
        data = self.client.get(reverse('products:api-v1-product-list'), {'category': 'Nope', 'page': 'abc', 'page_size': 999}).json()
        self.assertEqual(data['count'], 3)
        self.assertEqual(data['page'], 1)

    def test_on_sale_filter_and_sale_fields(self):
        data = self.client.get(reverse('products:api-v1-product-list'), {'on_sale': '1'}).json()
        self.assertEqual([p['name'] for p in data['results']], ['ThinkPad X1'])
        self.assertEqual(data['results'][0]['sale_price'], 1200000)
        self.assertEqual(data['results'][0]['discount_percentage'], 20)

    def test_detail_only_counts_published_reviews(self):
        data = self.client.get(reverse('products:api-v1-product-detail', args=[self.phone.id])).json()
        self.assertEqual(data['rating'], 4)
        self.assertEqual(data['review_count'], 1)
        self.assertEqual(len(data['reviews']), 1)
        self.assertEqual([p['name'] for p in data['related']], ['Nokia 105'])
        self.assertNotIn('password', str(data))

    def test_detail_reports_out_of_stock(self):
        data = self.client.get(reverse('products:api-v1-product-detail', args=[self.cheap_phone.id])).json()
        self.assertFalse(data['in_stock'])

    def test_missing_product_is_404(self):
        response = self.client.get(reverse('products:api-v1-product-detail', args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_api_is_read_only(self):
        response = self.client.post(reverse('products:api-v1-product-list'))
        self.assertEqual(response.status_code, 405)

    @override_settings(STOREFRONT_ORIGINS=['https://shop.example'])
    def test_cors_only_for_configured_storefront(self):
        url = reverse('products:api-v1-product-list')
        allowed = self.client.get(url, HTTP_ORIGIN='https://shop.example')
        self.assertEqual(allowed['Access-Control-Allow-Origin'], 'https://shop.example')
        blocked = self.client.get(url, HTTP_ORIGIN='https://evil.example')
        self.assertNotIn('Access-Control-Allow-Origin', blocked)
