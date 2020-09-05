from django.db.models import Count, Q
from hyp.models import Variant
from types import SimpleNamespace
import numpy as np

class ThompsonSampler:
    def __init__(self, experiment_id):
        self.experiment_id = experiment_id

    def variant(self):
        winner = max(
            self.samples(),
            key=lambda dict:dict["sampled_parameter"]
        )["variant"]

        # Convert dictionary to object so we can use dot notation to access its
        # properties
        return SimpleNamespace(**winner)

    def samples(self):
        interactions = self.interactions()
        conversions = self.conversions()

        samples = []
        for i in range(len(interactions)):
            alpha = conversions[i]["num_conversions"] + 1
            beta = interactions[i]["num_interactions"] - conversions[i]["num_conversions"] + 1

            result = {
                "variant": interactions[i],
                "sampled_parameter": np.random.beta(alpha, beta)
            }

            samples.append(result)

        return samples

    def interactions(self):
        return Variant.objects.values("id", "name").filter(
            experiment_id=self.experiment_id
        ).annotate(
            num_interactions=Count("interaction")
        )

    def conversions(self):
        return Variant.objects.values("id", "name").filter(
            experiment_id=self.experiment_id
        ).annotate(
            num_conversions=Count(
                "interaction", filter=Q(interaction__converted=True)
            )
        )
