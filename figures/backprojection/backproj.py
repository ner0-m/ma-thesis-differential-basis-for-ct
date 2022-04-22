#!/usr/bin/env python


import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Different examples of sinograms")
parser.add_argument("path", type=Path, default=1)


args = parser.parse_args()


def load_edf():
    import importlib.util

    spec = importlib.util.spec_from_file_location("edf", "../../scripts/edf.py")
    edf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(edf)
    return edf


def back_projection(ax, num):
    edf = load_edf()
    phantom = edf.readedf(args.path)

    from skimage.transform import radon, iradon
    import numpy as np

    theta = np.linspace(0., 180., num, endpoint=False,)
    sinogram = radon(phantom, theta=theta, circle=False)
    reconstruction = iradon(sinogram, theta=theta, filter_name=None, circle=False)

    ax.imshow(reconstruction, cmap="gray")
    # plt.show()


if __name__ == "__main__":
    for i in [1, 2, 4, 8, 32, 64, 128, 256, 512]:

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        back_projection(ax, i)
        ax.axis('off')
        plt.savefig(
            f"backprojection_{args.path.stem}_{str(i).zfill(3)}.png",
            bbox_inches="tight",
            pad_inches=0,
        )
    # plt.show()
