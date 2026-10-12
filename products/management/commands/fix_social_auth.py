from decouple import config
from django.core.management.base import BaseCommand, CommandError
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Fix duplicate social auth apps and register them properly'

    def handle(self, *args, **options):
        providers = (
            ('google', 'Google', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET'),
            ('github', 'GitHub', 'GITHUB_CLIENT_ID', 'GITHUB_CLIENT_SECRET'),
        )
        missing = [
            variable
            for _, _, client_id_env, secret_env in providers
            for variable in (client_id_env, secret_env)
            if not config(variable, default='')
        ]
        if missing:
            raise CommandError(
                'Set the required OAuth environment variables: '
                + ', '.join(missing)
            )

        current_site = Site.objects.get_current()
        for provider, name, client_id_env, secret_env in providers:
            existing_apps = SocialApp.objects.filter(provider=provider).order_by('pk')
            social_app = existing_apps.first()
            if social_app is None:
                social_app = SocialApp(provider=provider)

            social_app.name = name
            social_app.client_id = config(client_id_env)
            social_app.secret = config(secret_env)
            social_app.save()
            social_app.sites.set([current_site])
            existing_apps.exclude(pk=social_app.pk).delete()
            self.stdout.write(
                self.style.SUCCESS(f'{name} OAuth app registered')
            )

        self.stdout.write(self.style.SUCCESS('All social apps fixed!'))
        self.stdout.write(self.style.SUCCESS('\nFinal Social Apps:'))
        for app in SocialApp.objects.all():
            self.stdout.write(f'  - {app.provider}: {app.name}')
