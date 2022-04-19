#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser()

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


def plot_abdomen_with_projection(image, ax):
    import numpy as np
    from scipy.ndimage import rotate

    # Create projections
    from skimage.transform import radon

    angle = 0
    sinogram = radon(image, theta=[90 + angle])

    image = rotate(image, angle=-angle, reshape=False)

    ax.imshow(image, cmap="gray", vmin=0, vmax=1)
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
    return ax


def abdomen():
    import numpy as np

    edf = load_edf()
    abdo = edf.readedf("abdomen_512_normalized.edf")
    # cut away the left side
    image = np.zeros_like(abdo)
    image[50:430, 50:370] = abdo[50:430, 50:370]
    return image


def shepp_logan():
    import numpy as np

    edf = load_edf()
    image = edf.readedf("shepplogan.edf")
    return image


if __name__ == "__main__":
    edf = load_edf()
    image = abdomen()
    # image = shepp_logan()

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax = plot_abdomen_with_projection(image, ax)

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    import numpy as np
    from scipy.fft import fft2, fftshift

    fft = np.abs(fftshift(fft2(image)))
    print(np.min(fft), np.max(fft))

    x = np.linspace(0, 512, 512)
    y = np.linspace(0, 512, 512)
    sigmax, sigmay = 10, 10
    cy, cx = 256, 256
    X, Y = np.meshgrid(x, y)
    gmask = np.exp(-(((X - cx) / sigmax) ** 2 + ((Y - cy) / sigmay) ** 2))

    ftimagep = fft * gmask

    ax.imshow(ftimagep, cmap="gray")
    ax.plot([0, 512], [512, 0], color=colors["red"], lw=3)

    ax.set_xlim(0, 512)
    ax.set_ylim(0, 512)
    ax.xaxis.set_ticks_position("top")
    ax.yaxis.set_ticks_position("right")
    ax.axis("off")
    ax.invert_yaxis()

    plt.show()
