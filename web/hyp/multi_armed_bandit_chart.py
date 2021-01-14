import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from hyp.thompson_sampler import ThompsonSampler


class MultiArmedBanditChart:
    def __init__(self, conversion_rates, num_interactions=1000):
        self.conversion_rates = conversion_rates
        self.x_ticks = np.arange(0, num_interactions)[::250]
        self.x_points = np.arange(0, num_interactions)[::10]

    def plot(self):
        self.calculate_traffic_splits()

        fig = plt.figure(figsize=(9, 6))
        plt.suptitle("Traffic split by variant")
        plt.ylim(0.0, 1.0)
        plt.xlim(0, self.x_points[-1] + 10)
        plt.xticks(self.x_ticks)

        subplots = []

        for i in range(len(self.conversion_rates)):
            if i == 0:
                subplots.append(plt.subplot(
                    1,
                    len(self.conversion_rates),
                    i + 1,
                    xlabel="Unique visitors",
                    ylabel="Traffic percentage"
                ))
            else:
                subplots.append(plt.subplot(
                    1,
                    len(self.conversion_rates),
                    i + 1,
                    xlabel="Unique visitors",
                    sharey=subplots[0]
                ))

            plt.title(f'{int(self.conversion_rates[i] * 100)}% conversion rate')
            plt.plot(self.x_points, self.traffic_splits[:, i])

        return plt

    def calculate_traffic_splits(self):
        splits = []

        for num_interactions in self.x_points:
            variants = self.variants(num_interactions)
            sampler = ThompsonSampler(variants)
            traffic_splits = [
                percentage for percentage in sampler.simulated_traffic_split().values()
            ]
            splits.append(traffic_splits)

        self.traffic_splits = np.array(splits)

        return True

    def variants(self, num_interactions):
        return [
            {
                "id": i + 1,
                "num_conversions": self.conversion_rates[i] * num_interactions,
                "num_interactions": num_interactions
            } for i in range(len(self.conversion_rates))
        ]
