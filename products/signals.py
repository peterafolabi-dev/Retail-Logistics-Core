from django.db.models.signals import post_migrate
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from decouple import config
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender='products.Product')
def generate_product_description(sender, instance, created, raw=False, **kwargs):
    if not created or raw or (instance.description or '').strip():
        return

    try:
        from products.ai_descriptions import generate_description
        description = generate_description(instance)
        if description:
            sender.objects.filter(pk=instance.pk).update(description=description)
    except Exception:
        logger.exception('Could not generate description for new product %s', instance.pk)


@receiver(post_save, sender='products.Order')
def reward_referrer_on_first_paid_order(sender, instance, raw=False, **kwargs):
    if raw or not instance.is_paid:
        return
    try:
        from products.referrals import pay_referral_reward
        pay_referral_reward(instance)
    except Exception:
        logger.exception('Could not pay referral reward for order %s', instance.pk)


try:
    from allauth.account.signals import user_signed_up

    @receiver(user_signed_up)
    def record_social_signup_referral(sender, request, user, **kwargs):
        from products.referrals import record_referral
        record_referral(request, user)
except ImportError:  # allauth not installed
    pass


@receiver(post_migrate)
def create_default_site(sender, **kwargs):
    """Create the default Site object after migrations."""
    if sender.name == 'django.contrib.sites':
        site_url = config('SITE_URL', default='http://localhost:8000')
        domain = site_url.replace('https://', '').replace('http://', '').rstrip('/')
        site_name = 'Retail Logistics Core'

        Site.objects.get_or_create(
            pk=1,
            defaults={
                'domain': domain,
                'name': site_name,
            }
        )
