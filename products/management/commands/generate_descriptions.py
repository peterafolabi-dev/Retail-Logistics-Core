import logging
import time

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.db.models.functions import Trim

from products.ai_descriptions import generate_description
from products.models import Product

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate and save descriptions for products with empty descriptions.'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=25, help='Maximum number of products to process.')
        parser.add_argument('--dry-run', action='store_true', help='Report matching products without generating descriptions.')
        parser.add_argument('--force', action='store_true', help='Regenerate descriptions even when one already exists.')

    def handle(self, *args, **options):
        if args:
            raise CommandError('This command does not accept positional arguments.')

        limit = options['limit']
        if limit < 1:
            raise CommandError('--limit must be a positive integer.')

        products = Product.objects.all()
        if not options['force']:
            products = products.annotate(
                _trimmed_description=Trim('description')
            ).filter(
                Q(description__isnull=True) | Q(_trimmed_description='')
            )

        products = list(products.order_by('pk')[:limit])
        if options['dry_run']:
            self.stdout.write(f'Would generate descriptions for {len(products)} product(s).')
            return

        succeeded = 0
        for index, product in enumerate(products):
            try:
                description = generate_description(product)
                if description:
                    Product.objects.filter(pk=product.pk).update(description=description)
                    succeeded += 1
                else:
                    logger.warning('Skipping product %s: description generation returned no result.', product.pk)
            except Exception:
                logger.exception('Skipping product %s after description generation failed.', product.pk)

            if index < len(products) - 1:
                time.sleep(2)

        self.stdout.write(f'Generated descriptions for {succeeded} of {len(products)} product(s).')
