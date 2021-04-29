from django.test import Client
from hyp.models import HypUser
from allauth.account.models import EmailAddress


def signup(email, password, customer):
    client = Client()
    client.post('/accounts/signup/', {
        'email': email,
        'password1': password,
        'password2': password
    }, follow=True)

    email = EmailAddress.objects.filter(email=email, verified=False).first()
    email.verified = True
    email.save()

    user = HypUser.objects.get(email=email)
    user.customer = customer
    user.save()


def login(client, email, password):
    client.post('/accounts/login/', {'login': email, 'password': password}, follow=True)
