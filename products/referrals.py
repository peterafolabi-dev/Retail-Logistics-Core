"""Customer referral program.

Each user gets a personal link (/products/r/<code>/). The code is the user's id
plus a short HMAC, so it is stable, needs no database column and cannot be
forged for someone else. A visitor who signs up through the link is recorded
as referred; when their first order is paid the referrer gets wallet credit.
"""
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36

logger = logging.getLogger(__name__)

SESSION_KEY = 'referral_code'
_SALT = 'products.referrals'


def _signature(user_id):
    return salted_hmac(_SALT, str(user_id)).hexdigest()[:8]


def referral_code_for(user):
    return f'{int_to_base36(user.pk)}-{_signature(user.pk)}'


def referral_url_for(request, user):
    return request.build_absolute_uri(reverse('products:referral', args=[referral_code_for(user)]))


def referrer_from_code(code):
    """Return the active User a code belongs to, or None if it is invalid."""
    try:
        encoded_id, signature = str(code).split('-', 1)
        user_id = base36_to_int(encoded_id)
    except (ValueError, TypeError):
        return None
    if not constant_time_compare(signature, _signature(user_id)):
        return None
    return User.objects.filter(pk=user_id, is_active=True).first()


def reward_amount():
    return float(getattr(settings, 'REFERRAL_REWARD_AMOUNT', 1000))


def record_referral(request, new_user):
    """Link a newly registered user to the referrer stored in their session, if any."""
    from .models import Referral

    code = request.session.pop(SESSION_KEY, None)
    if not code:
        return None
    referrer = referrer_from_code(code)
    if referrer is None or referrer.pk == new_user.pk:
        return None
    try:
        with transaction.atomic():
            return Referral.objects.create(referrer=referrer, referred_user=new_user)
    except IntegrityError:
        # Already referred (the OneToOne on referred_user); keep the first referrer.
        return None


def pay_referral_reward(order):
    """Credit the referrer once, when the referred customer's first order is paid."""
    from .models import Referral, Wallet, WalletTransaction

    if not order.is_paid:
        return False
    with transaction.atomic():
        referral = (
            Referral.objects.select_for_update()
            .filter(referred_user_id=order.user_id, reward_paid=False)
            .first()
        )
        if referral is None:
            return False
        amount = reward_amount()
        wallet, _ = Wallet.objects.select_for_update().get_or_create(user=referral.referrer)
        wallet.deposit(amount)
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type='reward',
            amount=amount,
            reference=f'referral-{referral.pk}',
            description=f'Referral reward: {order.user.get_username()} placed their first order.',
        )
        referral.reward_paid = True
        referral.save(update_fields=['reward_paid'])
    logger.info('Paid referral reward %s to user %s for order %s', amount, referral.referrer_id, order.pk)
    return True
