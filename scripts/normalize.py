#!/usr/bin/env python

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Read file and create plot including window bar"
)
parser.add_argument("path", type=Path, help="Path to edf file to be windowed")
parser.add_argument(
    "--from-elsa", action=argparse.BooleanOptionalAction, help="Show figure"
)

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
    output_normalized = path.parents[0].joinpath(Path(stem + "_normalized.png"))
    output_edf = path.parents[0].joinpath(Path(stem + "_normalized.edf"))

    import edf
    import numpy as np

    data = edf.readedf(path, from_elsa=args.from_elsa)
    data = (data - np.min(data)) / np.ptp(data)
    edf.writeedf(data, output_edf)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    im = ax.imshow(np.rot90(np.fliplr(data), k=1), cmap="gray")
    ax.axis("off")
    plt.savefig(output_normalized, bbox_inches="tight", pad_inches=0)
