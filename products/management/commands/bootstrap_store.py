"""One-time store setup that is safe to run on every deploy.

Loads the product catalog from data.json when the database has no products,
and points the Sites framework (used in password-reset links) at SITE_URL.
Used as the deploy step on hosts without a shell (e.g. Vercel's build).
"""
import json
from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sites.models import Site
from django.core import serializers
from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = "Load the product catalog if empty and set the site domain."

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write(f"Products already exist ({Product.objects.count()}), skipping catalog load")
        else:
            fixture = json.loads((Path(settings.BASE_DIR) / "data.json").read_text(encoding="utf-8"))
            records = [item for item in fixture if item.get("model") == "products.product"]
            for obj in serializers.deserialize("json", json.dumps(records)):
                obj.save()
            self.stdout.write(f"Loaded {len(records)} products from data.json")

        domain = urlparse(settings.SITE_URL).netloc or "localhost:8000"
        Site.objects.update_or_create(id=1, defaults={"domain": domain, "name": "RedCart"})
        self.stdout.write(f"Site domain set to {domain}")
