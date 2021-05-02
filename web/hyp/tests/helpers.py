from django.test import Client
from hyp.models import HypUser
from allauth.account.models import EmailAddress

DEFAULT_PASSWORD = "this-is-a-very-nice-password-hooray!" # noqa S105


def signup(email, customer=None, password=DEFAULT_PASSWORD):
    client = Client()
    client.post('/accounts/signup/', {
        'email': email,
        'password1': password,
        'password2': password
    }, follow=True)

    email = EmailAddress.objects.filter(email=email, verified=False).first()
    email.verified = True
    email.save()

    if customer is not None:
        user = HypUser.objects.get(email=email)
        user.customer = customer
        user.save()


def login(client, email, password=DEFAULT_PASSWORD):
    client.post('/accounts/login/', {'login': email, 'password': password}, follow=True)
