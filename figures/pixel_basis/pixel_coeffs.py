import numpy as np
from scipy import signal, misc
import matplotlib.pyplot as plt


def pixel(x):
    y = np.zeros(x.shape)

    y[np.abs(x) < 0.5] = 1
    return y


def pixel_k(x, k, delta):
    return pixel(x / delta - k)


def pixel_coeffs(s):
    return s


def compute_basis_functions(num_samples, delta, ck):
    size = 150

    y_i = np.zeros((num_samples, size))
    x = np.linspace(-np.pi, 3 * np.pi, size)
    for i in range(num_samples):
        y_i[i] = ck[i] * pixel_k(x, i, delta)

    return y_i, np.tile(x, (num_samples, 1))


def sampled_function(sample_points):
    return 3 * np.sin(sample_points)

colors = {
    "red": "#DC267F",
    "blue": "#648FFF",
    "2": "#785EF0",
    "3": "#FE6100",
}

def sample_space(start, end, num=20):
    ks = np.linspace(start, end, num=num)
    return ks, (ks[1] - ks[0])


def plot_pixel_basis_fn(ax):
    x = np.linspace(-0.75, 0.75, 300)
    y = pixel(x)
    ax.plot(x, y, color=colors["red"])

    return x

def gen_fig_bspline_transformation(figure_path):
    num_samples = 10
    ks, delta = sample_space(0, 2 * np.pi, num=num_samples)
    ks_ref, _ = sample_space(0, 2 * np.pi, num=200)

    f = sampled_function(ks_ref)
    f_k = sampled_function(ks)

    ck = pixel_coeffs(f_k)
    ys, xs = compute_basis_functions(num_samples, delta, ck)

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(ks, f_k, "o", label="Sampled points", color=colors["red"])
    ax.plot(ks_ref, f, "--", label="True signal", color=colors["red"])
    ax.plot(xs[0], np.sum(ys, axis=0), "-", label="Approximation", color=colors["blue"])

    ax.set_xlim([-1, 7])
    # ax.set_ylim([-1.1, 1.1])
    ax.legend(loc="upper right")
    nice_axes(ax)

    if not figure_path:
        plt.show()
    else:
        plt.savefig(f"{figure_path}/pixel_transformation.png")


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

    ax.locator_params(axis="x", nbins=4)
    ax.locator_params(axis="y", nbins=2)

    return ax
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Argument parser")
parser.add_argument("--output", type=Path)


def main():
    args = parser.parse_args()
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    nice_axes(ax)
    plot_pixel_basis_fn(ax)

    if args.output:
        plt.savefig(f"{args.output}/pixel_basis.png")
    gen_fig_bspline_transformation(args.output)


if __name__ == "__main__":
    main()
