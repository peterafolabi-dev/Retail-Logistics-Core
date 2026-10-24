from django.core.management.base import BaseCommand

from products.catalog_descriptions import DESCRIPTIONS, build_description
from products.models import Product

# Earlier bulk-generated copy began with this heading and reused one paragraph
# per category, so it is treated as a placeholder that can be replaced.
GENERIC_PREFIX = 'Product overview\n'


class Command(BaseCommand):
    help = 'Fill missing or placeholder product descriptions from the curated catalogue.'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Overwrite every catalogue product, even with custom copy.')
        parser.add_argument('--dry-run', action='store_true', help='Report what would change without saving.')

    def handle(self, *args, **options):
        updated = 0
        for product in Product.objects.filter(name__in=DESCRIPTIONS.keys()):
            current = (product.description or '').strip()
            is_placeholder = not current or current.startswith(GENERIC_PREFIX)
            if not (options['force'] or is_placeholder):
                continue

            description = build_description(product.name)
            if description == current:
                continue
            if not options['dry_run']:
                Product.objects.filter(pk=product.pk).update(description=description)
            updated += 1

        missing = Product.objects.filter(description__regex=r'^\s*$').count()
        verb = 'Would update' if options['dry_run'] else 'Updated'
        self.stdout.write(f'{verb} {updated} product description(s). {missing} product(s) still without one.')
