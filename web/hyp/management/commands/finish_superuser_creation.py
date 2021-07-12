from django.core.management.base import BaseCommand, CommandError
from allauth.account.models import EmailAddress
from hyp.models import Customer, HypUser

class Command(BaseCommand):
    help = 'Assigns a customer to and verifies the email address of the most recently created superuser'

    def add_arguments(self, parser):
        # parser.add_argument(
        #     '--email',
        #     action='store_true',
        pass

    def handle(self, *args, **options):
        user = HypUser.objects.filter(is_staff=True).last()

        customer = Customer.objects.first()
        if customer is None:
            customer = Customer(name="A very cool customer")
            customer.save()

        user.customer = customer
        user.save()
        email = EmailAddress(email=user.email, verified=True, user_id=user.id)
        email.save()

        self.stdout.write(self.style.SUCCESS(f'Superuser {user.username} is ready to go!'))
