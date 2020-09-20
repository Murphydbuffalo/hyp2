from django.test import TestCase
from hyp.models import Customer, Experiment, Variant
from hyp.thompson_sampler import ThompsonSampler
import numpy as np

class TestThompsonSampler(TestCase):
    def setUp(self):
        np.random.seed(0)

        bonusly = Customer(name="Bonusly")
        bonusly.save()

        exp = Experiment(name="Trial lengths", customer=bonusly)
        exp.save()

        self.var1 = Variant(name="14 days", experiment=exp)
        self.var1.save()

        self.var2 = Variant(name="30 days", experiment=exp)
        self.var2.save()

        self.var3 = Variant(name="60 days", experiment=exp)
        self.var3.save()

    def test_uniform_prior(self):
        return True
