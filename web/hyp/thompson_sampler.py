import numpy as np


class ThompsonSampler:
    def __init__(self, variants):
        self.variants = variants

    def winner(self):
        return max(
            self.samples(),
            key=lambda dict: dict["sampled_parameter"]
        )["variant"]

    def simulated_traffic_split(self, n=1000):
        winner_counts = {v.id: 0 for v in self.variants}

        for _i in range(n):
            winner_counts[self.winner().id] += 1

        total = sum(winner_counts.values())

        return {id: winner_counts[id] / float(total) for id in winner_counts.keys()}

    # private

    def samples(self):
        samples = []
        for i in range(len(self.variants)):
            variant = self.variants[i]

            result = {
                "variant": variant,
                "sampled_parameter": np.random.beta(
                    self.alpha(variant), self.beta(variant)
                )
            }

            samples.append(result)

        return samples

    def alpha(self, variant):
        return variant.num_conversions + 1

    def beta(self, variant):
        return variant.num_interactions - variant.num_conversions + 1
