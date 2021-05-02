from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from hyp.models import Customer, Experiment, HypUser
from hyp.tests.helpers import login, signup


class TestExperiments(TestCase):
    def setUp(self):
        self.client = Client()
        bonusly = Customer(name="Bonusly")
        bonusly.save()
        wunder = Customer(name="Wunder")
        wunder.save()

        email = "dan@example.com"
        signup(email=email, customer=bonusly)
        login(client=self.client, email=email)

        e1 = Experiment(
            customer=bonusly,
            name="Test dank color schemes",
        )
        e1.save()
        e2 = Experiment(
            customer=bonusly,
            name="Chill vibez",
        )
        e2.save()
        e3 = Experiment(
            customer=wunder,
            name="wunderin bout choo",
        )
        e3.save()

    def test_index(self):
        response = self.client.get('/experiments/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Experiments', str(response.content))
        self.assertIn('Test dank color schemes', str(response.content))
        self.assertIn('Chill vibez', str(response.content))
        self.assertNotIn('wunerin bout choo', str(response.content))

    def test_auth(self):
        user = HypUser.objects.first()
        user.groups.first().permissions.remove(
            Permission.objects.get(codename="view_experiment")
        )

        response = self.client.get('/experiments/')
        self.assertEqual(response.status_code, 403)

        response = self.client.get(f'/experiments/{Experiment.objects.last().id}/')
        self.assertEqual(response.status_code, 403)
