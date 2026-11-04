from django.core.management.base import BaseCommand

from products.newsletter import send_daily_newsletter


class Command(BaseCommand):
    help = "Send today's newsletter (deal of the day, flash sales, new arrivals) to subscribers."

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=None, help='Send to at most this many subscribers.')

    def handle(self, *args, limit=None, **options):
        result = send_daily_newsletter(time_budget=10_000, limit=limit)
        self.stdout.write(self.style.SUCCESS(str(result)))
