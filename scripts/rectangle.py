#!/usr/bin/env python

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Read file and crop into given section")
parser.add_argument("path", type=Path, help="Path to edf file to be windowed")
parser.add_argument("--padding-left", type=int, default=0, help="")
parser.add_argument("--padding-top", type=int, default=0, help="")
parser.add_argument("--width", type=int, default=None, help="")
parser.add_argument("--height", type=int, default=None, help="")

args = parser.parse_args()

if __name__ == "__main__":
    path = args.path
    stem = path.stem
    output = path.parents[0].joinpath(Path(stem + "_rectangle.png"))

    import edf

    data = edf.readedf(path)

    padding_left = args.padding_left
    padding_top = args.padding_top
    width = args.width
    height = args.height

    if not width:
        width = data.shape[1]
    if not height:
        height = data.shape[0]

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    im = ax.imshow(data, cmap="gray")
    rect = patches.Rectangle(
        (padding_left, padding_top),
        width,
        height,
        linewidth=1,
        edgecolor="r",
        facecolor="none",
    )
    ax.add_patch(rect)
    plt.axis('off')
    plt.savefig(output, bbox_inches="tight", pad_inches=0)
