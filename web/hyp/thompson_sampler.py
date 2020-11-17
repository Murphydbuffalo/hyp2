from types import SimpleNamespace
import numpy as np

class ThompsonSampler:
    def __init__(self, variants):
        self.variants = variants

    def winner(self):
        winner = max(
            self.samples(),
            key=lambda dict:dict["sampled_parameter"]
        )["variant"]

        # Convert dictionary to object so we can use dot notation to access its
        # properties
        return SimpleNamespace(**winner)

    def samples(self):
        samples = []
        for i in range(len(self.variants)):
            variant = variants[i]
            alpha = variant["num_conversions"] + 1
            beta = variant["num_interactions"] - variant["num_conversions"] + 1

            result = {
                "variant": variant,
                "sampled_parameter": np.random.beta(alpha, beta)
            }

            samples.append(result)

        return samples
