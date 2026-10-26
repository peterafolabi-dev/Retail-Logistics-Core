import logging
import re
import uuid

from django.core.cache import cache
from django.db import IntegrityError
from django.utils import timezone

logger = logging.getLogger(__name__)

VISITOR_COOKIE = 'rc_vid'
VISITOR_COOKIE_AGE = 60 * 60 * 24 * 365  # one year
_SKIP_PATHS = re.compile(r'^/(static|media|admin|healthz|favicon\.ico|robots\.txt)|/api/')
_BOT_AGENTS = re.compile(r'bot|crawl|spider|slurp|curl|wget|python-requests|httpclient|monitor|uptime|render|headless|preview', re.I)
_COOKIE_VALUE = re.compile(r'^[0-9a-f]{32}$')


class VisitorTrackingMiddleware:
    """Record each real visitor once per day so the dashboard can show daily/monthly users.

    Only successful HTML page views count; static files, APIs, admin, health checks and bots
    are ignored. A cache check means at most one database write per visitor per day.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            self._track(request, response)
        except Exception:  # analytics must never break a page
            logger.exception('Visitor tracking failed')
        return response

    def _track(self, request, response):
        if request.method != 'GET' or response.status_code != 200:
            return
        if 'text/html' not in response.get('Content-Type', ''):
            return
        if _SKIP_PATHS.search(request.path) or _BOT_AGENTS.search(request.META.get('HTTP_USER_AGENT', '') or 'bot'):
            return

        user = getattr(request, 'user', None)
        if user is not None and user.is_authenticated:
            key = f'u:{user.pk}'
        else:
            anon_id = request.COOKIES.get(VISITOR_COOKIE, '')
            if not _COOKIE_VALUE.match(anon_id):
                anon_id = uuid.uuid4().hex
                response.set_cookie(VISITOR_COOKIE, anon_id, max_age=VISITOR_COOKIE_AGE,
                                    httponly=True, samesite='Lax', secure=request.is_secure())
            key = f'a:{anon_id}'
            user = None

        today = timezone.localdate()
        cache_key = f'visit:{today.isoformat()}:{key}'
        if cache.get(cache_key):
            return
        from .models import DailyVisitor
        try:
            DailyVisitor.objects.get_or_create(
                date=today, visitor_key=key,
                defaults={'user': user, 'first_path': request.path[:255]},
            )
        except IntegrityError:
            pass  # another request for the same visitor won the race
        cache.set(cache_key, True, 60 * 60 * 26)
