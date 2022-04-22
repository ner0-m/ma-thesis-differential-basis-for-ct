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


def filtered_sinogram(ax, filter="ramp"):
    from skimage.transform import radon, resize
    from skimage.transform.radon_transform import _get_fourier_filter
    import numpy as np
    from scipy.fft import fft, ifft

    edf = load_edf()
    phantom = edf.readedf(args.path)

    theta = np.linspace(
        0.0,
        180.0,
        np.max(phantom.shape),
        endpoint=False,
    )

    sino = radon(phantom, theta=theta, circle=False)
    sino = resize(sino, (512, 512))

    sino_shape = sino.shape[0]

    projection_size_padded = max(64, int(2 ** np.ceil(np.log2(2 * sino_shape))))
    pad_width = ((0, projection_size_padded - sino_shape), (0, 0))

    img = np.pad(sino, pad_width, mode="constant", constant_values=0)

    fourier_filter = _get_fourier_filter(projection_size_padded, filter)
    projection = fft(img, axis=0) * fourier_filter
    radon_filtered = np.real(ifft(projection, axis=0)[:sino_shape, :])

    ax.imshow(radon_filtered, cmap="gray")


def filtered_backprojection(ax, num):
    edf = load_edf()
    phantom = edf.readedf(args.path)

    from skimage.transform import radon, iradon
    import numpy as np

    theta = np.linspace(
        0.0,
        180.0,
        num,
        endpoint=False,
    )
    sinogram = radon(phantom, theta=theta, circle=False)
    reconstruction = iradon(sinogram, theta=theta, filter_name="cosine", circle=False)

    ax.imshow(reconstruction, cmap="gray")


def nice_axes(ax):
    # Move the left and bottom spines to x = 0 and y = 0, respectively.
    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))

    # Hide the top and right spines.
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # taken from https://stackoverflow.com/a/63936035
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    ax.locator_params(axis="x", nbins=4)
    ax.locator_params(axis="y", nbins=2)

    return ax


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # filters = ["ramp", "shepp-logan", "cosine", "hamming", "hann"]
    # filters = ["ramp"]
    # for filter in filters:
    #     fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    #     filtered_sinogram(ax, filter=filter)
    #     ax.axis("off")
    #     plt.savefig(
    #         f"fbp_{args.path.stem}_{filter}.png",
    #         bbox_inches="tight",
    #         pad_inches=0,
    #     )

    from skimage.transform.radon_transform import _get_fourier_filter

    colors = {
        "red": "#DC267F",
        "blue": "#648FFF",
        "2": "#785EF0",
        "3": "#FE6100",
    }

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    response = _get_fourier_filter(2000, "ramp")
    ax.plot(response, label="Ram-Lak", lw=5, color=colors["red"])
    response = _get_fourier_filter(2000, "shepp-logan")
    ax.plot(response, label="Shepp-Logan", lw=5, color=colors["blue"])

    ax.set_xlim([0, 1000])
    ax.set_ylim(bottom=0)
    ax.set_xlabel(r"$\omega$")
    ax.legend(loc="upper left", prop={'size': 18})
    # plt.show()
    nice_axes(ax)
    plt.savefig(
        f"fbp_filters.png",
        bbox_inches="tight",
        pad_inches=0,
    )

    # for i in [32, 64, 128, 256, 512]:
    #     fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    #     filtered_backprojection(ax, i)
    #     ax.axis("off")
    #     plt.savefig(
    #         f"fbp_{args.path.stem}_{str(i).zfill(3)}.png",
    #         bbox_inches="tight",
    #         pad_inches=0,
    #     )

    # plt.show()
