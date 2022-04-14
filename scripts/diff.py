#!/usr/bin/env python

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Read file and create plot including window bar"
)
parser.add_argument("truth", type=Path, help="Path to edf file to be windowed")
parser.add_argument("compare", type=Path, help="Path to edf file to be windowed")
parser.add_argument(
    "output", type=Path, help="Path and name of output files (without extension)"
)
parser.add_argument(
    "--normalize", action=argparse.BooleanOptionalAction, help="Normalize input first"
)
parser.add_argument("--show", action=argparse.BooleanOptionalAction, help="Show figure")

args = parser.parse_args()


def plot(data, ax, vmin=None, vmax=None):
    im = ax.imshow(data, cmap="gray", vmin=vmin, vmax=vmax)
    ax.axis("off")


def plot_windowed(data, ax, vmin=None, vmax=None):
    im = ax.imshow(data, cmap="gray", vmin=vmin, vmax=vmax)
    ax.axis("off")

    from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    cbbox = inset_axes(ax, "10%", "90%", loc="center right")
    cbbox.set_facecolor([1, 1, 1, 0.75])
    cbbox.set_xticks([])
    cbbox.set_yticks([])

    cbaxes = inset_axes(cbbox, "25%", "90%", loc="center left")
    cb = fig.colorbar(im, ax=ax, cax=cbaxes)


if __name__ == "__main__":
    ground_truth = args.truth
    compare = args.compare
    output = args.output
    stem = compare.stem

    outputedf = ground_truth.parents[0].joinpath(Path(f"{output}.edf"))
    outputpng = ground_truth.parents[0].joinpath(Path(f"{output}.png"))
    output_window = ground_truth.parents[0].joinpath(Path(f"{output}_windowed.png"))

    import edf

    x = edf.readedf(ground_truth)
    y = edf.readedf(compare)

    import numpy as np

    if args.normalize:
        x = (x - np.min(x)) / np.ptp(x)
        y = (y - np.min(y)) / np.ptp(y)

    diff = np.abs(x - y)
    diff = (diff - np.min(diff)) / np.ptp(diff)
    edf.writeedf(diff, outputedf)
    edf.savepng(diff, outputpng)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    plot_windowed(diff, ax)
    plt.savefig(output_window, bbox_inches="tight", pad_inches=0)
    if args.show:
        plt.show()
