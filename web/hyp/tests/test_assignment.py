from django.test import TestCase, Client
from hyp.models import ApiKey, Customer, Experiment, Interaction, Variant

class TestAssignment(TestCase):
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

    def test_consistent_assignment(self):
        query = Interaction.objects.filter(participant_id="danmurphy")
        self.assertEqual(query.count(), 0)

        response = self.client.post(
            f'/assign/danmurphy/{self.exp.id}',
            HTTP_X_HYP_TOKEN=self.access_token
        )

        variant = query.first().variant
        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.count(), 1)
        self.assertEqual(response.json()["id"], variant.id)
        self.assertEqual(response.json()["name"], variant.name)

        # Variant for a given participant does not change once assigned
        response = self.client.post(
            f'/assign/danmurphy/{self.exp.id}',
            HTTP_X_HYP_TOKEN=self.access_token
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.count(), 1)
        self.assertEqual(response.json()["id"], variant.id)
        self.assertEqual(response.json()["name"], variant.name)

    def test_no_variants_found(self):
        response = self.client.post(
            f'/assign/danmurphy/999',
            HTTP_X_HYP_TOKEN=self.access_token
        )
        self.assertEqual(response.status_code, 404)

    def test_bad_access_token(self):
        response = self.client.patch(f'/convert/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 401)

        response = self.client.patch(
            f'/convert/danmurphy/{self.exp.id}',
            HTTP_X_HYP_TOKEN="FOOEY"
        )

        self.assertEqual(response.status_code, 401)


    def test_unsupported_method(self):
        response = self.client.get(f'/assign/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)

        response = self.client.put(f'/assign/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(f'/assign/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(f'/assign/danmurphy/{self.exp.id}')
        self.assertEqual(response.status_code, 405)
