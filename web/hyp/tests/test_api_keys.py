from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from hyp.models import ApiKey, Customer, HypUser
from hyp.tests.helpers import login, signup


class TestApiKeys(TestCase):
    def setUp(self):
        self.client = Client()

        self.bonusly = Customer(name="Bonusly")
        self.bonusly.save()
        wunder = Customer(name="Wunder")
        wunder.save()
        self.wunder_key = ApiKey(customer=wunder, label="Wunder key")
        self.wunder_key.save()

        email = "dan@example.com"
        password = "ipulledintonazarethfeelingbouthalfpastdead" # noqa S105
        signup(email=email, password=password, customer=self.bonusly)
        login(client=self.client, email=email, password=password)

    def test_create_api_key(self):
        response = self.client.get('/api_keys/', follow=True)
        self.assertIn('API Keys', str(response.content))
        self.assertIn('Create API Key', str(response.content))
        self.assertNotIn((self.wunder_key.access_token), str(response.content))
        self.assertEqual(ApiKey.objects.count(), 1)

        response = self.client.post(
            '/api_keys/create',
            {"api_key_label": "My new key"},
            follow=True
        )
        self.assertEqual(ApiKey.objects.filter(customer_id=self.bonusly.id).count(), 1)
        key = ApiKey.objects.get(customer_id=self.bonusly.id)

        self.assertIn(str(key.access_token), str(response.content))
        self.assertIn(str(key.label), str(response.content))

        response = self.client.post(f'/api_keys/deactivate/{key.id}', follow=True)
        self.assertIn("Deactivated", str(response.content))
        key.refresh_from_db()
        self.assertFalse(key.is_active())

    def test_auth(self):
        user = HypUser.objects.get(email="dan@example.com")
        user.groups.first().permissions.remove(
            Permission.objects.get(codename="add_apikey")
        )

        key = ApiKey(customer=user.customer)
        key.save()

        self.assertEqual(ApiKey.objects.filter(customer=user.customer).count(), 1)

        response = self.client.get('/api_keys/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Create API Key', str(response.content))
        self.assertIn('Deactivate', str(response.content))

        response = self.client.post(
            '/api_keys/create',
            {"api_key_label": "My new key"},
            follow=True
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(ApiKey.objects.filter(customer=user.customer).count(), 1)

        user.groups.first().permissions.remove(
            Permission.objects.get(codename="change_apikey")
        )

        response = self.client.get('/api_keys/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Deactivate', str(response.content))
        self.assertTrue(key.is_active())

        response = self.client.patch(f'/api_keys/deactivate/{key.id}/')
        key.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertTrue(key.is_active())

        user.groups.first().permissions.remove(
            Permission.objects.get(codename="view_apikey")
        )
        response = self.client.get('/api_keys/', follow=True)

        self.assertEqual(response.status_code, 403)
        self.assertNotIn('API Keys', str(response.content))
