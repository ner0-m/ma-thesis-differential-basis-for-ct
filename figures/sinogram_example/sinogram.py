#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

from skimage.transform import radon, iradon


import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Different examples of sinograms")

parser.add_argument(
    "--single-abdomen-projection",
    action=argparse.BooleanOptionalAction,
    help="Compute single forward projection of abdomen",
)

parser.add_argument(
    "--sinogram-abdomen",
    action=argparse.BooleanOptionalAction,
    help="Compute single forward projection of abdomen",
)

parser.add_argument(
    "--sinogram-simple",
    action=argparse.BooleanOptionalAction,
    help="Compute single forward projection of abdomen",
)

parser.add_argument("--show", action=argparse.BooleanOptionalAction, help="Show figure")
parser.add_argument(
    "--angles", nargs="+", type=int, default=[0, 45, 90], help="Show figure"
)
args = parser.parse_args()


def load_edf():
    import importlib.util

    spec = importlib.util.spec_from_file_location("edf", "../../scripts/edf.py")
    edf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(edf)
    return edf


colors = {
    "red": "#DC267F",
    "blue": "#648FFF",
    "2": "#785EF0",
    "3": "#FE6100",
}


def abdomen_projection(angle):
    edf = load_edf()
    abdomen = edf.readedf("abdomen_512_normalized.edf")

    # cut away the left side
    image = np.zeros_like(abdomen)
    image[50:430, 50:370] = abdomen[50:430, 50:370]

    from scipy.ndimage import rotate

    # Create projections
    sinogram = radon(image, theta=[90 + angle])

    image = rotate(image, angle=-angle, reshape=False)

    # start with a square Figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    ax.imshow(image, cmap="gray_r", vmin=0, vmax=1)
    col = colors["red"]
    ax.plot(
        0.4 * np.flip(sinogram) + 512 - 64,
        np.linspace(0, sinogram.shape[0], sinogram.shape[0]),
        color=col,
    )

    ax.set_xlim(0, 512)
    ax.set_ylim(0, 512)
    ax.xaxis.set_ticks_position("top")
    ax.yaxis.set_ticks_position("right")

    ax.axis("off")
    ax.invert_yaxis()

    # Draw arrows
    x = 64
    for y in np.linspace(64, 512 - 64, 24, dtype=np.int32, endpoint=False)[1:]:
        plt.arrow(
            x,
            y,
            # 256 + 64 + 64,
            512 - 64 - x,
            0,
            lw=2,
            length_includes_head=True,
            head_width=2,
            fc=colors["red"],
            ec=colors["red"],
        )
    plt.savefig(
        f"abdomen_sinogram_{angle}.png",
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
    )
    plt.show()


def sinogram_abdomen():
    edf = load_edf()
    abdomen = edf.readedf("abdomen_512_normalized.edf")

    # cut away the left side
    image = np.zeros_like(abdomen)
    image[50:430, 50:370] = abdomen[50:430, 50:370]

    sinogram = radon(image, theta=np.linspace(0, 360, 512))
    print(sinogram.shape)

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.imshow(image, cmap="gray")
    ax.axis("off")

    plt.savefig(
        f"abdomen_512.png",
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
    )
     
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.imshow(sinogram, cmap="gray")
    ax.axis("off")

    ax.axvline(90, color=colors["red"])
    ax.axvline(90 + 45, color=colors["red"])
    ax.axvline(180, color=colors["red"])
    ax.axis("off")

    plt.savefig(
        f"abdomen_sinogram.png",
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
    )
    if args.show:
        plt.show()


def sinogram_simple():
    edf = load_edf()
    abdomen = edf.readedf("abdomen_512_normalized.edf")

    # cut away the left side
    image = np.zeros((512, 512))
    image[50:60, 320:330] = 1

    sinogram = radon(image, theta=np.linspace(0, 360, 512))

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.imshow(image, cmap="gray")
    ax.axis("off")

    plt.savefig(
        f"simple_phatom.png",
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
    )

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.imshow(sinogram, cmap="gray")
    ax.axis("off")
    plt.savefig(
        f"simple_sinogram.png",
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
    )
    if args.show:
        plt.show()


if __name__ == "__main__":
    if args.single_abdomen_projection:
        for angle in args.angles:
            abdomen_projection(angle)
    if args.sinogram_abdomen:
        sinogram_abdomen()
    if args.sinogram_simple:
        sinogram_simple()
