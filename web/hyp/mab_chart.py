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
fig, ax = plt.subplots(1, 3, figsize=(9, 6))
x, y = [], []
x_points = np.arange(1000)
y_points = [np.sin(point) for point in x_points]

lines = [line.plot(x, y, lw=2) for line in ax]

for axis in ax:
    axis.set_ylim(0.0, 1.0)
    axis.set_xlim(0, 1000)


def animate(i):
    x.append(x_points[i])
    y.append(y_points[i])

    for axis in ax:
        axis.figure.canvas.draw()

    for line in lines:
        # Only one line per subplot for now
        line[0].set_data(x, y)

    return lines


animation = FuncAnimation(fig, animate, interval=10)

plt.show()
