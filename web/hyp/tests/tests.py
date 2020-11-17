from django.test import TestCase
from hyp.models import Customer, Experiment, Variant
from hyp.thompson_sampler import ThompsonSampler
import numpy as np

class TestThompsonSampler(TestCase):
    def setUp(self):
        np.random.seed(0)

        bonusly = Customer(name="Bonusly")
        bonusly.save()

        self.exp = Experiment(name="Trial lengths", customer=bonusly)
        exp.save()

        self.var1 = Variant(name="14 days", experiment=self.exp)
        self.var1.save()

        self.var2 = Variant(name="30 days", experiment=self.exp)
        self.var2.save()

        self.var3 = Variant(name="60 days", experiment=self.exp)
        self.var3.save()

    # TODO:
    # test that if each variant has the same hardcoded conversion rate
    # each one gets selected roughly the same number of times, given
    # a high number of iterations. (Def want to query once and pass
    # in, rather than query each time, otherwise that'll be slow)
    #
    # Test out various conversion rates to make sure the variant
    # with the highest rate ends up getting nearly all the traffic
    # eventually
    #
    # More nuanced, but can also test that early on, after only a few
    # iterations, even suboptimal variants are getting at least some traffic
    def test_uniform_prior(self):
        return True
