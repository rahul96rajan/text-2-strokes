import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def plot_stroke(stroke, save_name=None):
    # Plot a single example.
    f, ax = plt.subplots()
    x = np.cumsum(stroke[:, 1])
    y = np.cumsum(stroke[:, 2])

    size_x = x.max() - x.min() + 1.0
    size_y = y.max() - y.min() + 1.0

    f.set_size_inches(5.0 * size_x / size_y, 5.0)

    cuts = np.where(stroke[:, 0] == 1)[0]
    start = 0

    for cut_value in cuts:
        ax.plot(x[start:cut_value], y[start:cut_value], "k-", linewidth=3)
        start = cut_value + 1

    ax.axis("off")  # equal
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    if save_name is None:
        plt.show()
    else:
        try:
            plt.savefig(save_name, bbox_inches="tight", pad_inches=0.5)
        except Exception:
            print("Error building image!: " + save_name)

    plt.close()


def plot_stroke_gif(stroke, save_name=None):
    fig, ax = plt.subplots()

    x = np.cumsum(stroke[:, 1])
    y = np.cumsum(stroke[:, 2])

    ax.set_xlim([min(x), max(x)])
    ax.set_ylim([min(y), max(y)])
    ax.axis("off")  # equal
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    size_x = x.max() - x.min() + 1.0
    size_y = y.max() - y.min() + 1.0
    fig.set_size_inches(5.0 * size_x / size_y, 5.0)

    cuts = np.where(stroke[:, 0] == 1)[0]

    x[cuts] = None
    y[cuts] = None

    def animate_frame(i):
        ax.plot(x[:i], y[:i], 'k-', linewidth=3)

    pts_per_frame = np.linspace(1, x.shape[0] + 1, cuts.shape[0]*4).astype(int)
    animation = FuncAnimation(fig, func=animate_frame,
                              frames=pts_per_frame, interval=100)

    if save_name is None:
        plt.show()
    else:
        try:
            writer = PillowWriter(fps=10)
            animation.save(save_name, writer=writer)
        except Exception:
            print("Error building image!: " + save_name)

    plt.close()
