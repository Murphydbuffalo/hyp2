from django.test import TestCase
from django_rq import get_worker
from hyp.jobs.variant_metrics import enqueue_all
from hyp.models import Customer, DailyVariantMetrics, Experiment, Variant


class TestVariantMetricsJob(TestCase):
    def setUp(self):
        bonusly = Customer(name="Bonusly")
        bonusly.save()

        self.exp = Experiment(name="Trial lengths", customer=bonusly)
        self.exp.save()

        self.var1 = Variant(name="14 days", experiment=self.exp, customer=bonusly)
        self.var1.save()

        self.var2 = Variant(name="30 days", experiment=self.exp, customer=bonusly)
        self.var2.save()

        self.var3 = Variant(name="60 days", experiment=self.exp, customer=bonusly)
        self.var3.save()

    def test_enqueue_all(self):
        self.assertEqual(DailyVariantMetrics.objects.count(), 0)

        jobs = enqueue_all()
        get_worker().work(burst=True)

        self.assertEqual(len(jobs), 3)
        self.assertEqual(DailyVariantMetrics.objects.count(), 3)

        # Test job is idempotent
        jobs = enqueue_all()
        get_worker().work(burst=True)

        self.assertEqual(len(jobs), 0)
        self.assertEqual(DailyVariantMetrics.objects.count(), 3)
