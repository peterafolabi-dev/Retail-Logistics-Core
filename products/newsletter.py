"""The daily RedCart newsletter: deal of the day, live flash sales and new arrivals.

Sent by a scheduled job (Vercel Cron → /products/cron/daily-newsletter/) or by
`python manage.py send_daily_newsletter`. Safe to run more than once a day:
each subscriber gets at most one email per day.
"""
import logging
import time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Newsletter, Product
from .utils import _email_context, _plain_text

logger = logging.getLogger(__name__)


def _in_stock(qs):
    from django.db.models import Q
    return qs.filter(Q(stock_quantity__gt=0) | Q(stock_quantity__isnull=True, stock__gt=0))


def build_digest(now=None):
    """Picks today's products. The deal of the day rotates by date so every day is different."""
    now = now or timezone.now()
    in_stock = _in_stock(Product.objects.all())
    flash = list(in_stock.filter(sale_price__isnull=False, sale_ends_at__gt=now).order_by('sale_ends_at')[:6])
    flash = [p for p in flash if p.has_active_sale][:4]
    new = list(in_stock.order_by('-id')[:4])
    pool = list(in_stock.order_by('id').values_list('id', flat=True))
    deal = None
    if pool:
        deal = Product.objects.get(id=pool[now.toordinal() % len(pool)])
    return {'deal': deal, 'flash_sales': flash, 'new_arrivals': new, 'date': now}


def build_message(subscriber, digest):
    site = (getattr(settings, 'SITE_URL', '') or '').rstrip('/')
    deal = digest.get('deal')
    if deal is not None:
        # email clients need absolute image URLs
        src = deal.image_src
        deal.email_img = src if src.startswith(('http://', 'https://')) else f"{site}{src if src.startswith('/') else '/' + src}"
    unsubscribe_url = f"{site}/products/newsletter/unsubscribe/{subscriber.ensure_token()}/"
    context = _email_context({**digest, 'email': subscriber.email, 'unsubscribe_url': unsubscribe_url})
    html = render_to_string('emails/daily_digest.html', context)
    subject = f"Today at RedCart: {deal.name}" if deal else 'Today at RedCart'
    msg = EmailMultiAlternatives(
        subject=subject,
        body=_plain_text(html),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[subscriber.email],
        headers={
            # lets Gmail and others show their own "Unsubscribe" button
            'List-Unsubscribe': f'<{unsubscribe_url}>',
            'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
        },
    )
    msg.attach_alternative(html, 'text/html')
    return msg


def send_daily_newsletter(now=None, time_budget=50.0, limit=None):
    """Sends today's email to every subscriber who hasn't had it yet.

    Stops early when the time budget runs out (serverless functions have a time limit);
    the next run carries on where this one stopped.
    """
    now = now or timezone.now()
    # "today" in Nigerian time (settings.TIME_ZONE), not UTC
    start_of_day = timezone.localtime(now).replace(hour=0, minute=0, second=0, microsecond=0)
    due = Newsletter.objects.filter(subscribed=True).exclude(last_sent_at__gte=start_of_day).order_by('id')
    if limit:
        due = due[:limit]
    digest = build_digest(now)
    if not digest['deal']:
        return {'sent': 0, 'failed': 0, 'remaining': due.count(), 'skipped': 'no products in stock'}

    started = time.monotonic()
    sent = failed = 0
    for sub in due:
        if time.monotonic() - started > time_budget:
            break
        try:
            build_message(sub, digest).send()
        except Exception:
            failed += 1
            logger.exception('Daily newsletter failed for subscriber %s', sub.pk)
            continue
        sub.last_sent_at = now
        sub.save(update_fields=['last_sent_at'])
        sent += 1
    remaining = Newsletter.objects.filter(subscribed=True).exclude(last_sent_at__gte=start_of_day).count()
    logger.info('Daily newsletter: %s sent, %s failed, %s remaining', sent, failed, remaining)
    return {'sent': sent, 'failed': failed, 'remaining': remaining}
