import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create or update the deployment superuser from environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not email or not password:
            self.stdout.write(self.style.WARNING(
                'Skipping superuser setup: DJANGO_SUPERUSER_USERNAME, '
                'DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD must be set.'
            ))
            return

        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        identifier = email if username_field == 'email' else username
        user = user_model._default_manager.filter(
            **{username_field: identifier}
        ).first()

        if user:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            if any(field.name == 'email' for field in user_model._meta.fields):
                user.email = email
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Updated deployment superuser: {identifier}'
            ))
            return

        user_fields = {
            username_field: identifier,
            'password': password,
        }
        if username_field != 'email' and any(
            field.name == 'email' for field in user_model._meta.fields
        ):
            user_fields['email'] = email

        user_model._default_manager.create_superuser(**user_fields)
        self.stdout.write(self.style.SUCCESS(
            f'Created deployment superuser: {identifier}'
        ))
