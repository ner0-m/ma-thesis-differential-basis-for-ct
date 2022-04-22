import numpy as np
from math import factorial
from scipy.special import binom
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Implementation based on
# Fast B-Spline Transformation for Continois Image Representation and Interpolation
# By Michael Unser (1991), equation 2.2
# Uses a shift
def bspline(x, n):
    xs = x + (n + 1) / 2
    res = np.zeros_like(np.asarray(x))
    for j in range(0, n + 2):  # till n+1 but make it inclusive therefore n + 2
        tmp1 = np.heaviside(xs - j, 0)
        tmp2 = np.power((xs - j), n)
        tmp3 = binom(n + 1, j)
        tmp4 = np.power(-1, j) / factorial(n)
        res += tmp4 * tmp3 * tmp2 * tmp1
    return res


# Based on A new representation and projection model for tomography, based on separable B-spline
# by Momey (2011)
# Equation after (7)
def nd_bspline(x, n):
    """
    Get a list of n-dimensional points x and the desired B-Spline basis function of degree n
    Return the function values of the B-Spline basis function of degree n at positions in x
    """
    res = np.ones(x.shape[0], dtype=np.float32)
    for elem in x.T:
        res *= bspline(elem, n)
    return res


colors = {
    "red": "#DC267F",
    "blue": "#648FFF",
    "purple": "#785EF0",
    "orange": "#FE6100",
}


# Based on https://en.wikipedia.org/wiki/B-spline#Derivative_expressions
# But I should check that reference and quote that :-D
# TODO: Extend to nd
def bspline_deriv(x, n):
    b_spline = bspline(x, n - 1)
    return b_spline[:-1] - b_spline[1:]


def bsplines_1d():
    x = np.linspace(-2, 2, 500)

    for d in range(0, 4):
        fig, ax = plt.subplots(1, 1, figsize=(20, 10))
        nice_axes(ax)
        ax.plot(
            x,
            bspline(x, d),
            label=f"B-Spline degree {d}",
            color=list(colors.values())[d],
            lw=5
        )
        plt.locator_params(nbins=4)
        fig.savefig(f"bspline_basis_1d_order{d}.png", bbox_inches="tight", pad_inches=0)


def bsplines_2d():
    size = 50
    # taken from https://stackoverflow.com/a/32208788
    raw = np.mgrid[-size : size + 1, -size : size + 1] / (size / 2)
    xy = raw.reshape(2, -1).T

    b = nd_bspline(xy, 3)
    print(xy.shape)
    print(b.shape)
    b_img = b.reshape(raw.shape[1:])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(raw[0], raw[1], b_img)
    plt.show()


def bsplines_derivative():
    x = np.linspace(-2, 2, 200)

    b = bspline_deriv(x, 2)
    fig = plt.figure()
    plt.plot(x[:-1], b, label="B-Spline degree 0")
    plt.legend(loc="lower right")
    plt.show()


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

    # ax.set_aspect("equal", "box")
    # ax.set_aspect("image")
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-0.1, 1.1)

    return ax


def main():
    bsplines_1d()
    # bsplines_2d()
    # bsplines_derivative()


if __name__ == "__main__":
    main()
