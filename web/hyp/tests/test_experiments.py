from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from hyp.models import Customer, Experiment, HypUser, Interaction, Variant
from hyp.tests.helpers import login, signup

import random
import re

class TestExperiments(TestCase):
    def converted(self, conversion_rate):
        return random.random() <= conversion_rate

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

        # Simulate different conversion rates for each variant
        self.conversion_rates = {}

        for i in range(3):
            v = Variant(name=f'Variant {i + 1}', experiment=e1, customer=e1.customer)
            v.save()
            self.conversion_rates[v.id] = 0.3 - (i * 0.1)

        self.experiment = e1

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

        response = self.client.post('/experiments/create/')
        self.assertEqual(response.status_code, 403)

    def test_experiment_detail_page(self):
        response = self.client.get(f'/experiments/{self.experiment.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test dank color schemes experiment', str(response.content))
        self.assertIn('No one has participated in this experiment yet.', str(response.content))
        self.assertIn('Uncertainty level: High', str(response.content))
        self.assertIn('Variant 1', str(response.content))
        self.assertIn('Variant 2', str(response.content))
        self.assertIn('Variant 3', str(response.content))
        self.assertIn('No one has interacted with this variant yet.', str(response.content))

        for _i in range(20):
            for j in range(3):
                variant = self.experiment.variant_set.all()[j]
                converted = self.converted(self.conversion_rates[variant.id])

                interaction = Interaction(
                    customer=self.experiment.customer,
                    experiment=self.experiment,
                    variant=variant,
                    participant_id=f'User {random.random()}',
                    converted=converted,
                )
                interaction.save()

        response = self.client.get(f'/experiments/{self.experiment.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test dank color schemes experiment', str(response.content))
        self.assertIn('60 unique participants.', str(response.content))
        self.assertIn('Uncertainty level: Moderate', str(response.content))
        self.assertIn('Variant 1', str(response.content))
        self.assertIn('Variant 2', str(response.content))
        self.assertIn('Variant 3', str(response.content))

        traffic_split_regexp = re.compile('Has received (\d+)% of traffic to date.')
        self.assertRegex(str(response.content), traffic_split_regexp)

        conversion_rate_regexp = re.compile('(\d+)% conversion rate.')
        self.assertRegex(str(response.content), conversion_rate_regexp)

    def test_create_success(self):
        response = self.client.get('/experiments/new/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('New Experiment', str(response.content))
        self.assertIn(
            '<form method="post" id="new-experiment-form" action="/experiments/create/">',
            str(response.content)
        )
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
        self.assertEqual(
            Experiment.objects.filter(name="hiii", customer_id=self.bonusly.id).count(),
            1
        )
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

    def test_description(self):
        self.assertEqual(self.experiment.description(), "Test dank color schemes")
        self.experiment.stopped = True
        self.experiment.save()
        self.assertEqual(self.experiment.description(), "Test dank color schemes (paused)")

    def test_total_interactions(self):
        self.assertEqual(self.experiment.total_interactions(), 0)
        interaction1 = Interaction(
            customer=self.experiment.customer,
            experiment=self.experiment,
            variant=self.experiment.variant_set.first(),
            participant_id="foo",
        )
        interaction1.save()
        interaction2 = Interaction(
            customer=self.experiment.customer,
            experiment=self.experiment,
            variant=self.experiment.variant_set.last(),
            participant_id="bar",
        )
        interaction2.save()

        self.assertEqual(self.experiment.total_interactions(), 2)

    def test_uncertainty_level(self):
        self.assertEqual(self.experiment.uncertainty_level(), "High")

        for _i in range(20):
            variant = self.experiment.variant_set.all()[0]
            converted = self.converted(self.conversion_rates[variant.id])

            interaction = Interaction(
                customer=self.experiment.customer,
                experiment=self.experiment,
                variant=variant,
                participant_id=f'User {random.random()}',
                converted=converted,
            )
            interaction.save()

        # Little uncertainty for the first variant, but still much uncertainty
        # for the other two
        self.assertEqual(self.experiment.uncertainty_level(), "High")

        for _i in range(20):
            variant = self.experiment.variant_set.all()[1]
            converted = self.converted(self.conversion_rates[variant.id])

            interaction = Interaction(
                customer=self.experiment.customer,
                experiment=self.experiment,
                variant=variant,
                participant_id=f'User {random.random()}',
                converted=converted,
            )
            interaction.save()

        # Still uncertainty in the last variant
        self.assertEqual(self.experiment.uncertainty_level(), "High")

        for _i in range(20):
            variant = self.experiment.variant_set.all()[2]
            converted = self.converted(self.conversion_rates[variant.id])

            interaction = Interaction(
                customer=self.experiment.customer,
                experiment=self.experiment,
                variant=variant,
                participant_id=f'User {random.random()}',
                converted=converted,
            )
            interaction.save()

        self.assertEqual(self.experiment.uncertainty_level(), "Moderate")

        for _i in range(20):
            for j in range(3):
                variant = self.experiment.variant_set.all()[j]
                converted = self.converted(self.conversion_rates[variant.id])

                interaction = Interaction(
                    customer=self.experiment.customer,
                    experiment=self.experiment,
                    variant=variant,
                    participant_id=f'User {random.random()}',
                    converted=converted,
                )
                interaction.save()

        self.assertEqual(self.experiment.uncertainty_level(), "Low")

    def traffic_split_history(self):
        pass

    def test_variant_conversion_rate(self):
        variant = self.experiment.variant_set.first()
        self.assertEqual(variant.conversion_rate(), 0.0)

        for _i in range(10):
            interaction = Interaction(
                customer=self.experiment.customer,
                experiment=self.experiment,
                variant=variant,
                participant_id=f'User {random.random()}',
            )
            interaction.save()

        variant.refresh_from_db()
        self.assertEqual(variant.conversion_rate(), 0.0)

        interactions = Interaction.objects.all()
        for i in range(5):
            interaction = interactions[i]
            interaction.converted = True
            interaction.save()

        variant.refresh_from_db()
        self.assertEqual(variant.conversion_rate(), 0.5)

    def test_variant_traffic_split_to_date(self):
        variants = self.experiment.variant_set.all()
        for variant in variants:
            self.assertEqual(variant.traffic_split_to_date(), 0.0)

        for _i in range(10):
            interaction = Interaction(
                customer=self.experiment.customer,
                experiment=self.experiment,
                variant=variants[0],
                participant_id=f'User {random.random()}',
            )
            interaction.save()

        variants[0].refresh_from_db()
        self.assertEqual(variants[0].traffic_split_to_date(), 1.0)

        variants[1].refresh_from_db()
        self.assertEqual(variants[1].traffic_split_to_date(), 0.0)

        variants[2].refresh_from_db()
        self.assertEqual(variants[2].traffic_split_to_date(), 0.0)

        for _i in range(10):
            interaction = Interaction(
                customer=self.experiment.customer,
                experiment=self.experiment,
                variant=variants[1],
                participant_id=f'User {random.random()}',
            )
            interaction.save()

        variants[0].refresh_from_db()
        self.assertEqual(variants[0].traffic_split_to_date(), 0.5)

        variants[1].refresh_from_db()
        self.assertEqual(variants[1].traffic_split_to_date(), 0.5)

        variants[2].refresh_from_db()
        self.assertEqual(variants[2].traffic_split_to_date(), 0.0)
