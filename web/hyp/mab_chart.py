import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# This works
# fig = plt.figure(figsize=(9,6))
# x, y = [], []
# x_points = np.arange(1000)
# def animate(i):
#     x.append(x_points[i])
#     y.append(np.sin(x[i]))
#     plt.plot(x,y)
#
# animation = FuncAnimation(fig, animate, interval=200)
# fig.show()

# This works
x_ticks = np.arange(1000)[::250]
x = np.arange(1000)[::10]
y = np.array([[np.sin(point), np.cos(point), point] for point in x])

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
        axis.set_ylim(0.0, 1.0)
        axis.set_xlim(0, 1010)

        if index == 0:
            axis.set_ylabel("Traffic percentage")

        if index == 1:
            axis.set_xlabel("Unique visitors")


animation = FuncAnimation(
    fig,
    animate,
    interval=10,
    repeat=False,
    init_func=init
)

plt.show()
