from django.test import TestCase
from hyp.models import Customer, Experiment, Variant, Interaction
from hyp.thompson_sampler import ThompsonSampler


class TestThompsonSampler(TestCase):
    def createInteraction(self, variant, converted):
        self.latest_participant_id += 1

        Interaction(
            variant=variant,
            experiment=self.exp,
            customer=self.exp.customer,
            participant_id=self.latest_participant_id,
            converted=converted
        ).save()

    def getVariantsWithConversions(self):
        return Variant.objects.with_interaction_counts().values(
            "id",
            "name",
            "num_interactions",
            "num_conversions"
        )

    def setUp(self):
        bonusly = Customer(name="Bonusly")
        bonusly.save()

        self.latest_participant_id = 0

        self.exp = Experiment(name="Trial lengths", customer=bonusly)
        self.exp.save()

        self.var1 = Variant(name="14 days", experiment=self.exp, customer=bonusly)
        self.var1.save()

        self.var2 = Variant(name="30 days", experiment=self.exp, customer=bonusly)
        self.var2.save()

        self.var3 = Variant(name="60 days", experiment=self.exp, customer=bonusly)
        self.var3.save()

        self.winner_counts = {}
        self.winner_counts[self.var1.id] = 0
        self.winner_counts[self.var2.id] = 0
        self.winner_counts[self.var3.id] = 0

    def test_no_conversions(self):
        variants = self.getVariantsWithConversions()

        n = 1000
        for _i in range(n):
            sampler = ThompsonSampler(variants)
            self.winner_counts[sampler.winner()["id"]] += 1

        self.assertAlmostEqual(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var2.id],
            delta=75
        )

        self.assertAlmostEqual(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var3.id],
            delta=75
        )

        self.assertAlmostEqual(
            self.winner_counts[self.var2.id],
            self.winner_counts[self.var3.id],
            delta=75
        )

    def test_equal_number_of_conversions(self):
        for _i in range(50):
            self.createInteraction(self.var1, converted=False)
            self.createInteraction(self.var2, converted=False)
            self.createInteraction(self.var3, converted=False)

        for _i in range(50):
            self.createInteraction(self.var1, converted=True)
            self.createInteraction(self.var2, converted=True)
            self.createInteraction(self.var3, converted=True)

        variants = self.getVariantsWithConversions()

        n = 1000
        for _i in range(n):
            sampler = ThompsonSampler(variants)
            self.winner_counts[sampler.winner()["id"]] += 1

        self.assertAlmostEqual(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var2.id],
            delta=75
        )

        self.assertAlmostEqual(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var3.id],
            delta=75
        )

        self.assertAlmostEqual(
            self.winner_counts[self.var2.id],
            self.winner_counts[self.var3.id],
            delta=75
        )

    def test_higher_conversion_rate_with_little_uncertainty_wins_almost_always(self):
        # Below we create 100 interactions for each variant, with 25 successes
        # for variants 2 and 3, but 50 successes for variant 1.
        # After 100 trials the posterior distributions will have little uncertainty
        # remaining, and so sampling from them will almost always return something
        # quite close to the true conversion rate.
        for _i in range(50):
            self.createInteraction(self.var1, converted=False)

        for _i in range(50):
            self.createInteraction(self.var1, converted=True)

        for _i in range(75):
            self.createInteraction(self.var2, converted=False)
            self.createInteraction(self.var3, converted=False)

        for _i in range(25):
            self.createInteraction(self.var2, converted=True)
            self.createInteraction(self.var3, converted=True)

        variants = self.getVariantsWithConversions()

        n = 1000
        for _i in range(n):
            sampler = ThompsonSampler(variants)
            self.winner_counts[sampler.winner()["id"]] += 1

        self.assertGreater(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var2.id],
        )
        self.assertNotAlmostEqual(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var2.id],
            delta=900
        )

        self.assertGreater(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var3.id],
        )
        self.assertNotAlmostEqual(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var3.id],
            delta=900
        )

        self.assertAlmostEqual(
            self.winner_counts[self.var2.id],
            self.winner_counts[self.var3.id],
            delta=75
        )

    def test_higher_conversion_rate_with_much_uncertainty_wins_slightly_more(self):
        # Below we create 20 interactions for each variant, with 5 successes
        # for variants 2 and 3, but 10 successes for variant 1.
        # Even though the conversion rates are the same as in the previous test
        # after 20 trials the posterior distributions will still have some uncertainty
        # remaining, and so sampling from them will almost always return something
        # quite close to the true conversion rate.
        for _i in range(10):
            self.createInteraction(self.var1, converted=False)

        for _i in range(10):
            self.createInteraction(self.var1, converted=True)

        for _i in range(15):
            self.createInteraction(self.var2, converted=False)
            self.createInteraction(self.var3, converted=False)

        for _i in range(5):
            self.createInteraction(self.var2, converted=True)
            self.createInteraction(self.var3, converted=True)

        variants = self.getVariantsWithConversions()

        n = 1000
        for _i in range(n):
            sampler = ThompsonSampler(variants)
            self.winner_counts[sampler.winner()["id"]] += 1

        self.assertGreater(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var2.id],
        )
        self.assertNotAlmostEqual(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var2.id],
            delta=300
        )

        self.assertGreater(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var3.id],
        )
        self.assertNotAlmostEqual(
            self.winner_counts[self.var1.id],
            self.winner_counts[self.var3.id],
            delta=300
        )

        self.assertAlmostEqual(
            self.winner_counts[self.var2.id],
            self.winner_counts[self.var3.id],
            delta=75
        )
