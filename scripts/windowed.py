#!/usr/bin/env python

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Read file and create plot including window bar"
)
parser.add_argument("path", type=Path, help="Path to edf file to be windowed")
parser.add_argument("--min", help="Window Min")
parser.add_argument("--max", help="Window Max")
parser.add_argument("--show", action=argparse.BooleanOptionalAction, help="Show figure")

args = parser.parse_args()


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
    path = args.path
    stem = path.stem
    output_window = path.parents[0].joinpath(Path(stem + "_windowed.png"))
    min = args.min
    max = args.max

    import edf

    data = edf.readedf(path)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    plot_windowed(data, ax, vmin=min, vmax=max)

    plt.savefig(output_window, bbox_inches="tight", pad_inches=0)
    if args.show:
        plt.show()
