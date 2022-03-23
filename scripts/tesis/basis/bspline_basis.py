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


# Based on https://en.wikipedia.org/wiki/B-spline#Derivative_expressions
# But I should check that reference and quote that :-D
# TODO: Extend to nd
def bspline_deriv(x, n):
    b_spline = bspline(x, n - 1)
    return b_spline[:-1] - b_spline[1:]


def bsplines_1d():
    x = np.linspace(-2, 2, 200)
    b_0 = bspline(x, 0)
    b_1 = bspline(x, 1)
    b_2 = bspline(x, 2)
    b_3 = bspline(x, 3)

    fig = plt.figure()
    plt.plot(x, b_0, label="B-Spline degree 0")
    plt.plot(x, b_1, label="B-Spline degree 1")
    plt.plot(x, b_2, label="B-Spline degree 2")
    plt.plot(x, b_3, label="B-Spline degree 3")

    plt.legend(loc="lower right")
    plt.show()


def bsplines_2d():
    size = 50
    # taken from https://stackoverflow.com/a/32208788
    raw = np.mgrid[-size:size + 1, -size:size + 1] / (size / 2)
    xy = raw.reshape(2, -1).T

    b = nd_bspline(xy, 3)
    b_img = b.reshape(raw.shape[1:])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(raw[0], raw[1], b_img)
    plt.show()


def bsplines_derivative():
    x = np.linspace(-2, 2, 200)

    b = bspline_deriv(x, 2)
    fig = plt.figure()
    plt.plot(x[:-1], b, label="B-Spline degree 0")
    plt.legend(loc="lower right")
    plt.show()


def main():
    bsplines_derivative()


if __name__ == "__main__":
    main()
