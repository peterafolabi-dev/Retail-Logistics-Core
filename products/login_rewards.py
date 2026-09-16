"""
Daily login rewards for RedCart.

Design: a 7-day escalating reward cycle. Claiming is an explicit user
action (not silent auto-credit on login) — a visible "claim" moment is
what actually drives the retention benefit; silently crediting wallets
in the background gets no engagement value at all.

Streak rules:
- Claiming on the calendar day immediately after your last claim
  continues the streak and advances to the next day's reward.
- Missing a day (a gap of 2+ calendar days since your last claim)
  resets the streak back to day 1.
- Claiming again on the same calendar day is a no-op (already claimed).
- After day 7, the cycle wraps back to day 1's reward on the next claim.
"""
from datetime import timedelta
import logging

from django.utils import timezone

logger = logging.getLogger(__name__)

# Naira amount rewarded for each consecutive day in the cycle (1-indexed).
REWARD_SCHEDULE = [10, 15, 20, 30, 40, 60, 100]


def _reward_for_streak(streak_count):
    """streak_count is 1-indexed (day 1, day 2, ...). Wraps every 7 days."""
    index = (streak_count - 1) % len(REWARD_SCHEDULE)
    return REWARD_SCHEDULE[index]


def get_reward_status(user):
    """
    Returns a dict describing today's reward state for this user, without
    claiming anything — safe to call anytime to render UI.

    {
        'can_claim': bool,
        'current_streak': int,      # streak AFTER today's claim, if claimed
        'next_reward_amount': int,  # what claiming today would pay
        'already_claimed_today': bool,
    }
    """
    from .models import LoginRewardStreak  # local import avoids circular import at module load

    streak_obj, _ = LoginRewardStreak.objects.get_or_create(user=user)
    today = timezone.now().date()

    already_claimed_today = streak_obj.last_claimed_date == today

    if already_claimed_today:
        return {
            'can_claim': False,
            'current_streak': streak_obj.current_streak,
            'next_reward_amount': _reward_for_streak(streak_obj.current_streak + 1),
            'already_claimed_today': True,
        }

    if streak_obj.last_claimed_date == today - timedelta(days=1):
        prospective_streak = streak_obj.current_streak + 1
    else:
        prospective_streak = 1  # first claim ever, or streak broken by a missed day

    return {
        'can_claim': True,
        'current_streak': prospective_streak,
        'next_reward_amount': _reward_for_streak(prospective_streak),
        'already_claimed_today': False,
    }


def claim_daily_reward(user):
    """
    Claims today's reward if not already claimed, crediting the user's
    Wallet and advancing their streak. Returns a dict:
        {'success': bool, 'amount': int or None, 'new_streak': int, 'message': str}
    Safe to call even if already claimed today — returns success=False
    with an explanatory message rather than double-crediting.
    """
    from .models import LoginRewardStreak, Wallet, WalletTransaction

    streak_obj, _ = LoginRewardStreak.objects.get_or_create(user=user)
    today = timezone.now().date()

    if streak_obj.last_claimed_date == today:
        return {
            'success': False,
            'amount': None,
            'new_streak': streak_obj.current_streak,
            'message': "You've already claimed today's reward.",
        }

    if streak_obj.last_claimed_date == today - timedelta(days=1):
        new_streak = streak_obj.current_streak + 1
    else:
        new_streak = 1

    amount = _reward_for_streak(new_streak)

    wallet, _ = Wallet.objects.get_or_create(user=user)
    wallet.deposit(amount)
    WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type='reward',
        amount=amount,
        reference=f'DAILY-REWARD-{today.isoformat()}',
        description=f'Daily login reward — day {new_streak} of streak',
    )

    streak_obj.current_streak = new_streak
    streak_obj.longest_streak = max(streak_obj.longest_streak, new_streak)
    streak_obj.last_claimed_date = today
    streak_obj.save(update_fields=['current_streak', 'longest_streak', 'last_claimed_date'])

    logger.info('User %s claimed day-%d login reward: ₦%d', user.username, new_streak, amount)

    return {
        'success': True,
        'amount': amount,
        'new_streak': new_streak,
        'message': f'You claimed ₦{amount} for day {new_streak} of your streak!',
    }