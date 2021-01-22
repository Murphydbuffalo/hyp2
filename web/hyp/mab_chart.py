import numpy as np
from matplotlib import style, pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from hyp.thompson_sampler import ThompsonSampler


def calculate_traffic_splits(conversion_rates, x_points):
    splits = []

    for num_interactions in x_points:
        sampler = ThompsonSampler(variants(conversion_rates, num_interactions))
        traffic_splits = [
            percentage for percentage in sampler.simulated_traffic_split().values()
        ]
        splits.append(traffic_splits)

    return np.array(splits)


def variants(conversion_rates, num_interactions):
    return [
        {
            "id": i + 1,
            "num_conversions": conversion_rates[i] * num_interactions,
            "num_interactions": num_interactions
        } for i in range(len(conversion_rates))
    ]


conversion_rates = [0.05, 0.10, 0.03]
x_ticks = np.arange(1000)[::250]
x = np.arange(1000)[::25]
bandit_splits = calculate_traffic_splits(conversion_rates, x)
ab_test_splits = (np.zeros(bandit_splits.shape) + 1) * (1 / len(conversion_rates))

# After A/B test has completed
ab_test_splits[35:40, 0] = 0.0
ab_test_splits[35:40, 1] = 1.0
ab_test_splits[35:40, 2] = 0.0

style.use("seaborn")
fig, ax = plt.subplots(1, 3, figsize=(9, 6))
plt.suptitle("Traffic split by variant")

line_groups = [axis.plot([], [], 'b-', [], [], 'r--', lw=2) for axis in ax]


def animate(i):
    for _index, axis in enumerate(ax):
        axis.figure.canvas.draw()
        # axis.fill_between(
        #     x[0:i + 1],
        #     bandit_splits[0:i + 1, index],
        #     ab_test_splits[0:i + 1, index],
        #     color="yellow",
        #     alpha=0.3,
        #     animated=True
        # )

    for index, lines in enumerate(line_groups):
        lines[0].set_data(x[0:i + 1], bandit_splits[0:i + 1, index])
        lines[1].set_data(x[0:i + 1], ab_test_splits[0:i + 1, index])


def init():
    for index, axis in enumerate(ax):
        axis.set_xticks(x_ticks)
        axis.set_ylim(-0.05, 1.05)
        axis.set_xlim(0, 1010)
        axis.legend(["Hyp", "A/B Test"])
        axis.set_title(f"{conversion_rates[index] * 100}% conversion rate")

        if index == 0:
            axis.set_ylabel("Traffic percentage")

        if index == 1:
            axis.set_xlabel("Unique visitors")


animation = FuncAnimation(
    fig,
    animate,
    interval=200,
    repeat=True,
    init_func=init
)

plt.show()


def save_as_html(filename="traffic_splits.html"):
    try:
        html = animation.to_html5_video()
        f = open(filename, "w")
        f.write(html)
    finally:
        f.close()
        plt.close()


writer = PillowWriter(fps=30)
animation.save("traffic_splits.gif", writer=writer)
