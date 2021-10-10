import numpy as np

from scipy.stats import beta


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

    def uncertainty(self):
        if any([self.interval_width(v) >= 0.25 for v in self.variants]):
            return "High"
        elif any([self.interval_width(v) >= 0.10 for v in self.variants]):
            return "Moderate"
        else:
            return "Low"

    # private

    def samples(self):
        samples = []
        for i in range(len(self.variants)):
            variant = self.variants[i]

            result = {
                "variant": variant,
                "sampled_parameter": np.random.beta(self.alpha(variant), self.beta(variant))
            }

            samples.append(result)

        return samples

    def alpha(self, variant):
        return variant.num_conversions + 1

    def beta(self, variant):
        return variant.num_interactions - variant.num_conversions + 1

    def interval_width(self, variant, mass=0.97):
        interval_start, interval_end = beta.interval(mass, self.alpha(variant), self.beta(variant))

        return interval_end - interval_start
