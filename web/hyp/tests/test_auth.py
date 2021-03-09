from django.test import TestCase, Client
from django.core import mail
from django.contrib import auth
from hyp.models import HypUser
from allauth.account.models import EmailAddress
import re


class TestAuth(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup(self):
        self.assertEqual(EmailAddress.objects.count(), 0)
        self.assertEqual(HypUser.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.get('/accounts/signup/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertIn('<form action="/accounts/signup/" method="post">', str(response.content))
        self.assertIn('<input type="email" name="email"', str(response.content))
        self.assertIn('<input type="password" name="password1"', str(response.content))
        self.assertIn('<input type="password" name="password2"', str(response.content))

        response = self.client.post(
            '/accounts/signup/',
            {
                'email': 'bob@example.com',
                'password1': 'thisisaverynicepasswordfortesting!',
                'password2': 'thisisaverynicepasswordfortesting!'
            },
            follow=True
        )

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0], ('/accounts/confirm-email/', 302))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(HypUser.objects.filter(email='bob@example.com').count(), 1)
        self.assertEqual(
            EmailAddress.objects.filter(email='bob@example.com', verified=False).count(),
            1
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '[Hyp] Please Confirm Your E-mail Address')
        self.assertIn('Welcome to Hyp!', mail.outbox[0].body)
        self.assertIn('/accounts/confirm-email/', mail.outbox[0].body)

        confirmation_path_regexp = re.compile("(/accounts/confirm-email/.+/)")
        confirmation_path = confirmation_path_regexp.search(mail.outbox[0].body).group(1)

        response = self.client.get(confirmation_path, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            EmailAddress.objects.filter(email='bob@example.com', verified=True).count(),
            1
        )

    def test_login(self):
        self.client.post(
            '/accounts/signup/',
            {
                'email': 'bob@example.com',
                'password1': 'thisisaverynicepasswordfortesting!',
                'password2': 'thisisaverynicepasswordfortesting!'
            },
            follow=True
        )

        email = EmailAddress.objects.filter(email='bob@example.com', verified=False).first()
        email.verified = True
        email.save()

        bad_login_response = self.client.post(
            '/accounts/login/',
            {
                'login': 'bob@example.com',
                'password': 'notgonnahappen',
            },
            follow=True
        )

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.assertEqual(bad_login_response.status_code, 200)
        self.assertIn('errorlist', str(bad_login_response.content))
        self.assertIn(
            'The e-mail address and/or password you specified are not correct.',
            str(bad_login_response.content)
        )

        response = self.client.post(
            '/accounts/login/',
            {
                'login': 'bob@example.com',
                'password': 'thisisaverynicepasswordfortesting!',
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('errorlist', str(response.content))

        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        self.client.post(
            '/accounts/signup/',
            {
                'email': 'bob@example.com',
                'password1': 'thisisaverynicepasswordfortesting!',
                'password2': 'thisisaverynicepasswordfortesting!'
            },
            follow=True
        )

        email = EmailAddress.objects.filter(email='bob@example.com', verified=False).first()
        email.verified = True
        email.save()

        self.client.post(
            '/accounts/login/',
            {
                'login': 'bob@example.com',
                'password': 'thisisaverynicepasswordfortesting!',
            },
            follow=True
        )

        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated)

        self.client.post(
            '/accounts/logout/',
            {
                'login': 'bob@example.com',
                'password': 'thisisaverynicepasswordfortesting!',
            },
            follow=True
        )

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated)
