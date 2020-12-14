from django.test import TestCase, Client
from hyp.models import ApiKey, Customer, Experiment, Interaction, Variant

class TestConversion(TestCase):
    def setUp(self):
        self.client = Client()

        bonusly = Customer(name="Bonusly")
        bonusly.save()

        api_key = ApiKey(customer=bonusly, name="Assignment test key")
        api_key.save()
        self.access_token = "SANDBOX/" + api_key.access_token

        self.exp = Experiment(name="Trial lengths", customer=bonusly)
        self.exp.save()

        self.var1 = Variant(name="14 days", experiment=self.exp)
        self.var1.save()

        self.var2 = Variant(name="30 days", experiment=self.exp)
        self.var2.save()

        self.var3 = Variant(name="60 days", experiment=self.exp)
        self.var3.save()

    def test_conversion_updates_interaction(self):
        interaction = Interaction(
            experiment_id=self.exp.id,
            variant_id=self.var1.id,
            participant_id="danmurphy"
        )
        interaction.save()

        self.assertEqual(interaction.converted, False)

        response = self.client.patch(
            f'/api/v1/convert/danmurphy/{self.exp.id}',
            HTTP_X_HYP_TOKEN=self.access_token
        )

        interaction.refresh_from_db()

        self.assertEqual(interaction.converted, True)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(response.json()["payload"]["id"], self.exp.id)

    def test_no_interaction_found(self):
        response = self.client.patch(
            f'/api/v1/convert/danmurphy/{self.exp.id}',
            HTTP_X_HYP_TOKEN=self.access_token
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "No interaction matches that ID.")
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
        response = self.client.get(f'/api/v1/convert/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["message"], "That HTTP method isn't supported on this URL.")
        self.assertEqual(response.json()["payload"], "")

        response = self.client.post(f'/api/v1/convert/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(f'/api/v1/convert/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)
