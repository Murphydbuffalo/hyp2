import numpy as np

# TODO: allow user-defined priors to get to a low level of uncertainty faster?
# Eg could ask the user "do you have a rough estimate of what the conversion rate
# typically is for this type of feature?"
class ThompsonSampler:
    def __init__(self, variants):
        self.variants = variants

    def winner(self):
        return max(
            self.samples(),
            key=lambda dict:dict["sampled_parameter"]
        )["variant"]

    def samples(self):
        samples = []
        for i in range(len(self.variants)):
            variant = self.variants[i]
            alpha = variant["num_conversions"] + 1
            beta = variant["num_interactions"] - variant["num_conversions"] + 1

            result = {
                "variant": variant,
                "sampled_parameter": np.random.beta(alpha, beta)
            }

            samples.append(result)

        return samples
