from django.test import TestCase, Client
from hyp.models import ApiKey, Customer, Experiment, Interaction, Variant


class TestAssignment(TestCase):
    def setUp(self):
        self.client = Client()

        bonusly = Customer(name="Bonusly")
        bonusly.save()

        api_key = ApiKey(customer=bonusly, label="Assignment test key")
        api_key.save()
        self.access_token = str(api_key)

        self.exp = Experiment(name="Trial lengths", customer=bonusly)
        self.exp.save()

        self.var1 = Variant(name="14 days", experiment=self.exp, customer=bonusly)
        self.var1.save()

        self.var2 = Variant(name="30 days", experiment=self.exp, customer=bonusly)
        self.var2.save()

        self.var3 = Variant(name="60 days", experiment=self.exp, customer=bonusly)
        self.var3.save()

    def test_consistent_assignment(self):
        query = Interaction.objects.filter(participant_id="danmurphy")
        self.assertEqual(query.count(), 0)
        self.assertEqual(self.var1.num_interactions, 0)
        self.assertEqual(self.var1.num_conversions, 0)

        response = self.client.post(
            f'/api/v1/assign/danmurphy/{self.exp.id}',
            HTTP_X_HYP_TOKEN=self.access_token
        )

        variant = query.first().variant
        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.count(), 1)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(response.json()["payload"]["variant_id"], variant.id)
        self.assertEqual(response.json()["payload"]["variant_name"], variant.name)

        variant.refresh_from_db()
        self.assertEqual(variant.num_interactions, 1)
        self.assertEqual(variant.num_conversions, 0)

        # Variant for a given participant does not change once assigned
        response = self.client.post(
            f'/api/v1/assign/danmurphy/{self.exp.id}',
            HTTP_X_HYP_TOKEN=self.access_token
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.count(), 1)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(response.json()["payload"]["variant_id"], variant.id)
        self.assertEqual(response.json()["payload"]["variant_name"], variant.name)

        variant.refresh_from_db()
        self.assertEqual(variant.num_interactions, 1)
        self.assertEqual(variant.num_conversions, 0)

    def test_no_experiment_found(self):
        response = self.client.post(
            '/api/v1/assign/danmurphy/999',
            HTTP_X_HYP_TOKEN=self.access_token
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], (
            "No experiment with ID 999 was found."
        ))
        self.assertEqual(response.json()["payload"], "")

    def test_bad_access_token(self):
        response = self.client.patch(f'/api/v1/convert/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 401)

        response = self.client.patch(
            f'/api/v1/convert/danmurphy/{self.exp.id}',
            HTTP_X_HYP_TOKEN="FOOEY"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["message"], "Missing or invalid access token.")
        self.assertEqual(response.json()["payload"], "")

    def test_unsupported_method(self):
        response = self.client.get(f'/api/v1/assign/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["message"], (
            "That HTTP method isn't supported on this URL."
        ))
        self.assertEqual(response.json()["payload"], "")

        response = self.client.put(f'/api/v1/assign/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(f'/api/v1/assign/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(f'/api/v1/assign/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)
