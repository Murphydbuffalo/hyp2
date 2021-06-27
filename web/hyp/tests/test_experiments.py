from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from hyp.models import Customer, Experiment, HypUser
from hyp.tests.helpers import login, signup


class TestExperiments(TestCase):
    def setUp(self):
        self.client = Client()
        self.bonusly = Customer(name="Bonusly")
        self.bonusly.save()
        wunder = Customer(name="Wunder")
        wunder.save()

        email = "dan@example.com"
        signup(email=email, customer=self.bonusly)
        login(client=self.client, email=email)

        e1 = Experiment(
            customer=self.bonusly,
            name="Test dank color schemes",
        )
        e1.save()
        e2 = Experiment(
            customer=self.bonusly,
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
        user.groups.first().permissions.remove(
            Permission.objects.get(codename="add_experiment")
        )

        response = self.client.get('/experiments/new/')
        self.assertEqual(response.status_code, 403)

        response = self.client.post(f'/experiments/create/')
        self.assertEqual(response.status_code, 403)

    def test_create_success(self):
        response = self.client.get('/experiments/new/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('New Experiment', str(response.content))
        self.assertIn('<form method="post" id="new-experiment-form" action="/experiments/create/">', str(response.content))
        self.assertIn('<input type="text" name="name"', str(response.content))
        self.assertIn('<input type="text" name="variant_set-0-name"', str(response.content))
        self.assertIn('<input type="text" name="variant_set-1-name"', str(response.content))
        self.assertIn('Save', str(response.content))

        payload = {
            'name': ['hiii'],
            'variant_set-TOTAL_FORMS': ['2'],
            'variant_set-INITIAL_FORMS': ['0'],
            'variant_set-MIN_NUM_FORMS': ['2'],
            'variant_set-MAX_NUM_FORMS': ['10'],
            'variant_set-0-name': ['byee'],
            'variant_set-0-id': [''],
            'variant_set-0-experiment': [''],
            'variant_set-1-name': ['beee'],
            'variant_set-1-id': [''],
            'variant_set-1-experiment': [''],
        }

        response = self.client.post('/experiments/create/', payload, follow=True)
        self.assertEqual(Experiment.objects.filter(name="hiii", customer_id=self.bonusly.id).count(), 1)
        exp = Experiment.objects.get(customer_id=self.bonusly.id, name="hiii")
        variants = exp.variant_set.all()
        self.assertEqual(len(variants), 2)
        self.assertEqual(variants[0].name, "byee")
        self.assertEqual(variants[1].name, "beee")

    def test_create_fail_no_name(self):
        payload = {
            'name': [],
            'variant_set-TOTAL_FORMS': ['2'],
            'variant_set-INITIAL_FORMS': ['0'],
            'variant_set-MIN_NUM_FORMS': ['2'],
            'variant_set-MAX_NUM_FORMS': ['10'],
            'variant_set-0-name': ['byee'],
            'variant_set-0-id': [''],
            'variant_set-0-experiment': [''],
            'variant_set-1-name': ['beee'],
            'variant_set-1-id': [''],
            'variant_set-1-experiment': [''],
        }

        response = self.client.post('/experiments/create/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Experiment.objects.filter(customer_id=self.bonusly.id).count(), 2)
        self.assertIn('This field is required', str(response.content))

    def test_create_fail_no_variant_names(self):
        payload = {
            'name': ['Hello!'],
            'variant_set-TOTAL_FORMS': ['2'],
            'variant_set-INITIAL_FORMS': ['0'],
            'variant_set-MIN_NUM_FORMS': ['2'],
            'variant_set-MAX_NUM_FORMS': ['10'],
            'variant_set-0-name': [''],
            'variant_set-0-id': [''],
            'variant_set-0-experiment': [''],
            'variant_set-1-name': ['beee'],
            'variant_set-1-id': [''],
            'variant_set-1-experiment': [''],
        }

        response = self.client.post('/experiments/create/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Experiment.objects.filter(customer_id=self.bonusly.id).count(), 2)
        self.assertIn('This field is required.', str(response.content))

    def test_create_fail_duplicate_variant_names(self):
        payload = {
            'name': ['Hello!'],
            'variant_set-TOTAL_FORMS': ['2'],
            'variant_set-INITIAL_FORMS': ['0'],
            'variant_set-MIN_NUM_FORMS': ['2'],
            'variant_set-MAX_NUM_FORMS': ['10'],
            'variant_set-0-name': ['DUPLICATE'],
            'variant_set-0-id': [''],
            'variant_set-0-experiment': [''],
            'variant_set-1-name': ['DUPLICATE'],
            'variant_set-1-id': [''],
            'variant_set-1-experiment': [''],
        }
        response = self.client.post('/experiments/create/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Experiment.objects.filter(customer_id=self.bonusly.id).count(), 2)
        self.assertIn('Each variant must have a unique name.', str(response.content))


    def test_create_fail_duplicate_experiment_name(self):
        payload = {
            'name': ['Test dank color schemes'],
            'variant_set-TOTAL_FORMS': ['2'],
            'variant_set-INITIAL_FORMS': ['0'],
            'variant_set-MIN_NUM_FORMS': ['2'],
            'variant_set-MAX_NUM_FORMS': ['10'],
            'variant_set-0-name': ['byee'],
            'variant_set-0-id': [''],
            'variant_set-0-experiment': [''],
            'variant_set-1-name': ['beee'],
            'variant_set-1-id': [''],
            'variant_set-1-experiment': [''],
        }

        response = self.client.post('/experiments/create/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Experiment.objects.filter(customer_id=self.bonusly.id).count(), 2)
        self.assertIn('Experiment name is already taken.', str(response.content))
