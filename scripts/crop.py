#!/usr/bin/env python

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Read file and crop into given section")
parser.add_argument("path", type=Path, help="Path to edf file to be windowed")
parser.add_argument("--padding-left", type=int, default=0, help="")
parser.add_argument("--padding-top", type=int, default=0, help="")
parser.add_argument("--width", type=int, default=None, help="")
parser.add_argument("--height", type=int, default=None, help="")
parser.add_argument(
    "--windowed", action=argparse.BooleanOptionalAction, help="Show figure"
)
parser.add_argument(
    "--from-elsa", action=argparse.BooleanOptionalAction, help="Show figure"
)
parser.add_argument("--show", action=argparse.BooleanOptionalAction, help="Show figure")

args = parser.parse_args()


def plot_windowed(data, ax, vmin=None, vmax=None):
    import matplotlib.colors as colors

    im = ax.imshow(data, cmap="gray", vmin=vmin, vmax=vmax, norm=colors.Normalize())
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
    output = path.parents[0].joinpath(Path(stem + "_cropped.png"))

    import edf

    data = edf.readedf(path, from_elsa=args.from_elsa)

    padding_left = args.padding_left
    padding_top = args.padding_top
    width = args.width
    height = args.height

    if not width:
        width = data.shape[1]
    if not height:
        height = data.shape[0]

    import numpy as np

    cropped = data[
        padding_top : padding_top + height, padding_left : padding_left + width
    ]

    print(f"{output} windowed: [{np.min(cropped)}, {np.max(cropped)}]")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 1, figsize=(10, 10))
    import matplotlib.colors as colors

    im = axes.imshow(
        cropped,
        cmap="gray",
        norm=colors.Normalize(),
    )

    plt.axis("off")
    plt.savefig(output, bbox_inches="tight", pad_inches=0)

    if args.windowed:
        fig, axes = plt.subplots(1, 1, figsize=(10, 10))
        plot_windowed(cropped, axes)
        output = path.parents[0].joinpath(Path(stem + "_cropped_windowed.png"))
        plt.savefig(output, bbox_inches="tight", pad_inches=0)

    if args.show:
        plt.show()
