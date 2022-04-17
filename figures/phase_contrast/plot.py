#!/usr/bin/env python

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

args = parser.parse_args()

colors = {
    "reference": "k",
    "attenuated": "#DC267F",
    "phase": "#785EF0",
    "scatter": "#648FFF",
    "red": "#DC267F",
    "blue": "#648FFF",
    "2": "#785EF0",
    "3": "#FE6100",
}


def fn(x, amp, avg, phase):
    import numpy as np

    return amp * np.sin((x + phase)) + avg


def plot_fn(ax, fn, amplitude, avg, phase, color):
    import numpy as np

    end = 2.125 * np.pi
    x = np.arange(-0.125 * np.pi, end, np.pi / 32) + 0.25
    y = fn(x, amplitude, avg, phase)

    ax.plot(x, y, lw=3, color=color)

    return ax


ref_amplitude = 1
ref_average = ref_amplitude + 0.5
ref_phase = 0


def attenuated(ax):
    import numpy as np

    amplitude = ref_amplitude
    avg = ref_average - 0.25
    phase = ref_phase

    col = colors["attenuated"]
    ax = plot_fn(ax, fn, amplitude, avg, phase, col)
    ax.axhline(avg, linestyle="--", color=col)

    return ax


def phase(ax):
    import numpy as np

    amplitude = ref_amplitude
    avg = ref_average
    phase = -np.pi * 0.25

    col = colors["phase"]
    ax = plot_fn(ax, fn, amplitude, avg, phase, col)
    ax.axvline(0.5 * np.pi - phase, linestyle="--", color=col)
    return ax


def scattered(ax):
    import numpy as np

    amplitude = ref_amplitude * 0.6
    avg = ref_average
    phase = ref_phase

    col = colors["scatter"]
    ax = plot_fn(ax, fn, amplitude, avg, phase, col)
    ax.axhline(avg + amplitude, linestyle="--", color=col)
    ax.axhline(avg - amplitude, linestyle="--", color=col)
    return ax


def plot_reference(ax):
    import numpy as np

    amplitude = ref_amplitude
    avg = ref_average
    phase = ref_phase

    col = colors["reference"]
    ax = plot_fn(ax, fn, amplitude, avg, phase, col)
    return ax


def nice_axes(ax):
    # No labels
    ax.set_xticks([])
    ax.set_yticks([])

    # Move the left and bottom spines to x = 0 and y = 0, respectively.
    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))
    # Hide the top and right spines.
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # taken from https://stackoverflow.com/a/63936035
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    ax.set_aspect("equal", "box")

    ax.set_ylabel("intensity", loc="top")
    ax.set_xlabel("grating position", loc="right")

    return ax


def plot_attenuation():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    ax = nice_axes(ax)

    ax = plot_reference(ax)
    ax = attenuated(ax)
    ax.axhline(ref_average, linestyle="--", color=colors["reference"])

    plt.savefig(
        f"plot_attenuation.png",
        bbox_inches="tight",
        pad_inches=0,
        dpi=300,
    )


def plot_phase():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    ax = nice_axes(ax)

    ax = plot_reference(ax)
    ax = phase(ax)

    import numpy as np

    ax.axvline(0.5 * np.pi - ref_phase, linestyle="--", color=colors["reference"])

    plt.savefig(
        f"plot_phase.png",
        bbox_inches="tight",
        pad_inches=0,
        dpi=300,
    )


def plot_scattering():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    ax = nice_axes(ax)

    ax = plot_reference(ax)
    ax = scattered(ax)

    import numpy as np

    ax.axhline(ref_average + ref_amplitude, linestyle="--", color=colors["reference"])
    ax.axhline(ref_average - ref_amplitude, linestyle="--", color=colors["reference"])

    plt.savefig(
        f"plot_scattered.png",
        bbox_inches="tight",
        pad_inches=0,
        dpi=300,
    )


if __name__ == "__main__":
    plot_attenuation()
    plot_phase()
    plot_scattering()

    import matplotlib.pyplot as plt

    plt.show()
