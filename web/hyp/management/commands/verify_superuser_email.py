from django.core.management.base import BaseCommand, CommandError
from allauth.account.models import EmailAddress
from hyp.models import HypUser

class Command(BaseCommand):
    help = 'Verifies the email address of a superuser'

    def add_arguments(self, parser):
        # parser.add_argument(
        #     '--email',
        #     action='store_true',
        pass

    def handle(self, *args, **options):
        user = HypUser.objects.filter(is_staff=True).last()
        email = EmailAddress(email=user.email, verified=True, user_id=user.id)
        email.save()

        self.stdout.write(self.style.SUCCESS('Superuser email confirmed'))
