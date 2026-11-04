"""Staff view of who signed up: name, email, how they joined, orders and spend."""
import csv
from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Count, Exists, OuterRef, Q
from django.http import HttpResponse
from django.utils import timezone

PERIODS = {'today': 0, '7d': 6, '30d': 29}


def customer_queryset(params):
    """Users filtered by the page's search/period/method/newsletter controls."""
    from allauth.socialaccount.models import SocialAccount
    from .models import Newsletter

    qs = User.objects.annotate(
        via_google=Exists(SocialAccount.objects.filter(user=OuterRef('pk'), provider='google')),
        on_newsletter=Exists(Newsletter.objects.filter(email__iexact=OuterRef('email'), subscribed=True)),
        paid_orders=Count('orders', filter=Q(orders__is_paid=True), distinct=True),
    ).order_by('-date_joined')

    q = (params.get('q') or '').strip()
    if q:
        qs = qs.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
    period = params.get('period') or 'all'
    if period in PERIODS:
        since = timezone.localdate() - timedelta(days=PERIODS[period])
        qs = qs.filter(date_joined__date__gte=since)
    method = params.get('method') or ''
    if method == 'google':
        qs = qs.filter(via_google=True)
    elif method == 'email':
        qs = qs.filter(via_google=False)
    if params.get('newsletter') == '1':
        qs = qs.filter(on_newsletter=True)
    if params.get('buyers') == '1':
        qs = qs.filter(paid_orders__gt=0)
    return qs


def spend_by_user(user_ids):
    from .models import Order
    totals = {}
    for order in Order.objects.filter(user_id__in=user_ids, is_paid=True).prefetch_related('items'):
        totals[order.user_id] = totals.get(order.user_id, 0) + order.total
    return totals


def customers_csv(qs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="redcart-customers-{timezone.localdate()}.csv"'
    writer = csv.writer(response)
    writer.writerow(['username', 'first_name', 'last_name', 'email', 'joined', 'last_login', 'signed_up_with', 'paid_orders', 'total_spent_naira', 'newsletter', 'staff'])
    users = list(qs)
    spent = spend_by_user([u.id for u in users])
    for u in users:
        writer.writerow([
            u.username, u.first_name, u.last_name, u.email,
            timezone.localtime(u.date_joined).strftime('%Y-%m-%d %H:%M'),
            timezone.localtime(u.last_login).strftime('%Y-%m-%d %H:%M') if u.last_login else '',
            'Google' if u.via_google else 'Email',
            u.paid_orders, round(spent.get(u.id, 0), 2),
            'yes' if u.on_newsletter else 'no', 'yes' if u.is_staff else 'no',
        ])
    return response
