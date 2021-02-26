from django.test import TestCase, Client
from django.core import mail
from hyp.models import HypUser
from allauth.account.models import EmailAddress


class TestSignup(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ui_has_form(self):
        response = self.client.get('/accounts/signup/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertIn('<form action="/accounts/signup/" method="post">', str(response.content))
        self.assertIn('<input type="email" name="email"', str(response.content))
        self.assertIn('<input type="password" name="password1"', str(response.content))
        self.assertIn('<input type="password" name="password2"', str(response.content))

    def test_verification_sends_on_form_submit(self):
        self.assertEqual(EmailAddress.objects.count(), 0)
        self.assertEqual(HypUser.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

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
