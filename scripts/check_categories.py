import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywork.settings')
django.setup()

from products.models import Product

categories = Product.objects.values_list('category', flat=True).distinct()
for cat in sorted(categories):
    print(f"\n=== {cat} ===")
    products = Product.objects.filter(category=cat)
    for p in products:
        print(f"  {p.id}: {p.name}")