import argparse
from pathlib import Path

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
    return np.sin(sample_points)

def sample_space(start, end, num=20):
    ks = np.linspace(start, end, num=num)
    return ks, (ks[1] - ks[0])


def gen_fig_bspline_transformation(figure_path):
    num_samples = 10
    ks, delta = sample_space(0, 2 * np.pi, num=num_samples)
    f_k = sampled_function(ks)

    ck = pixel_coeffs(f_k)
    ys, xs = compute_basis_functions(num_samples, delta, ck)

    fig = plt.figure()
    plt.plot(ks, f_k, 'o', label="Sampled points")
    plt.plot(xs.T, ys.T, '--')
    plt.plot(xs[0], np.sum(ys, axis=0), '-', label="Approximation")

    plt.xlim([-2, 8])
    plt.ylim([-1.1, 1.1])
    plt.legend(loc="lower right")
     
    if not figure_path:
        plt.show()
    else:
        plt.savefig(f"{figure_path}/pixel_transformation.png")
         
    fig = plt.figure()
    plt.plot(ks, f_k, 'o', label="Sampled points")
    plt.xlim([-2, 8])
    plt.ylim([-1.1, 1.1])
    plt.legend(loc="lower right")
    if not figure_path:
        plt.show()
    else:
        plt.savefig(f"{figure_path}/raw_sample_points.png")
 
parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument("--figure-path", type=Path)
 
def main():
    args = parser.parse_args()
    gen_fig_bspline_transformation(args.figure_path)


if __name__ == "__main__":
    main()

