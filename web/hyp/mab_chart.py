import numpy as np
from matplotlib import style, pyplot as plt
from matplotlib.animation import FuncAnimation
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


x_ticks = np.arange(1000)[::250]
x = np.arange(1000)[::25]
y = calculate_traffic_splits([0.05, 0.10, 0.03], x)

style.use("seaborn")
fig, ax = plt.subplots(1, 3, figsize=(9, 6))
plt.suptitle("Traffic split by variant")

lines = [line.plot([], [], lw=2) for line in ax]


def animate(i):
    for axis in ax:
        axis.figure.canvas.draw()

    for index, line in enumerate(lines):
        # Only one line per subplot for now
        line[0].set_data(x[0:i + 1], y[0:i + 1, index])


def init():
    for index, axis in enumerate(ax):
        axis.set_xticks(x_ticks)
        axis.set_ylim(-0.05, 1.05)
        axis.set_xlim(0, 1010)

        if index == 0:
            axis.set_ylabel("Traffic percentage")

        if index == 1:
            axis.set_xlabel("Unique visitors")


animation = FuncAnimation(
    fig,
    animate,
    interval=333,
    repeat=False,
    init_func=init
)

plt.show()


def save_as_html():
    try:
        html = animation.to_html5_video()
        f = open("traffic_splits.html", "w")
        f.write(html)
    finally:
        f.close()
        plt.close()
