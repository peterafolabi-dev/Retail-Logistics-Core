from django.db import migrations


def deactivate_spin10(apps, schema_editor):
    # The cart "spin the wheel" game was removed; its code must stop working.
    Coupon = apps.get_model('products', 'Coupon')
    Coupon.objects.filter(code__iexact='SPIN10').update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_product_ai_description'),
    ]

    operations = [
        migrations.RunPython(deactivate_spin10, migrations.RunPython.noop),
    ]
