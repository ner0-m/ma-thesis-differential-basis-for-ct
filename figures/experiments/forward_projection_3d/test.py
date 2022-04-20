#!/usr/bin/env python

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="")
parser.add_argument("slice", type=int)
parser.add_argument("path", type=Path)
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


def load_edf():
    import importlib.util

    spec = importlib.util.spec_from_file_location("edf", "../../../scripts/edf.py")
    edf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(edf)
    return edf


if __name__ == "__main__":
    path = args.path
    slice = args.slice

    stem = path.stem
    output = path.parents[0].joinpath(Path(f"{stem}_{slice}.png"))
    print(output)

    edf = load_edf()
    data = edf.readedf(path, from_elsa=True)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    plot_windowed(data[slice, :, :], ax)
    plt.savefig(output, bbox_inches="tight", pad_inches=0)
