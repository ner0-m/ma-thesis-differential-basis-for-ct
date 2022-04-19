#!/usr/bin/env python

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

args = parser.parse_args()

colors = {
    "red": "#DC267F",
    "blue": "#648FFF",
    "purple": "#785EF0",
    "orange": "#FE6100",
}


def nice_axes(ax):

    # Move the left and bottom spines to x = 0 and y = 0, respectively.
    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))
    # Hide the top and right spines.
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # taken from https://stackoverflow.com/a/63936035
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    ax.set_aspect("equal", "box")
    # ax.legend(loc="upper right")
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = True

    return ax


def blob(r, m, alpha, a):
    from scipy.special import iv
    import numpy as np

    if len(r.shape) == 2:
        r = np.abs(np.linalg.norm(r, axis=1))

    if alpha == 0:
        return (1 - (r / a) ** 2) ** m

    s = np.sqrt(1 - (r / a) ** 2)
    iv1 = iv(m, alpha * s)
    iv2 = iv(m, alpha)
    return np.where(r > a, 0, iv1 / iv2 * (s**m))


def plot_blob(ax, m, alpha, a, color):
    import numpy as np

    x = np.linspace(0, a, 100)
    y = blob(x, m, alpha, a)

    ax.plot(x, y, color=color, label=rf"{m = }, $\alpha = {alpha}$")

def plot_2dblob(ax, m, alpha, a):
    import numpy as np
    import matplotlib.pyplot as plt
    size = 50
    # taken from https://stackoverflow.com/a/32208788
    raw = np.mgrid[-size:size + 1, -size:size + 1] / (size / 2)
    xy = raw.reshape(2, -1).T

    b = blob(xy, m, alpha, a)
    b_img = b.reshape(raw.shape[1:])

    ax.imshow(b_img, cmap="gray_r")


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # ax = nice_axes(ax)
    ax.axis('off')
    plot_2dblob(ax, 2, 10.83, 2)
    plt.savefig(
        f"blob_2d.png",
        bbox_inches="tight",
        pad_inches=0,
        dpi=300,
    )

    for m in range(0, 3):
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        ax = nice_axes(ax)

        plot_blob(ax, m, 0, 2, colors["orange"])
        plot_blob(ax, m, 4, 2, colors["purple"])
        plot_blob(ax, m, 8, 2, colors["red"])
        plot_blob(ax, m, 10.83, 2, colors["blue"])

        ax.legend(loc="upper right", fontsize=16)
        plt.savefig(
            f"blob_alphas_order_{m}.png",
            bbox_inches="tight",
            pad_inches=0,
            dpi=300,
        )

    # plt.show()
