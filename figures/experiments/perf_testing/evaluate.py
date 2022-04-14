#!/usr/bin/env python


def read_csv(filename, kind):
    import csv

    data = {}
    with open(filename, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";")
        for row in spamreader:
            projector = row[0]
            size = row[2]

            if row[1] != kind:
                continue

            subitem = {
                "kind": row[1],
                "angles": row[3],
                "runs": row[4],
                "warmups": row[5],
                "data": np.array(row[6:-2]).astype(np.float64),
            }

            if projector not in data:
                data[projector] = {}

            if size not in data[projector]:
                data[projector][size] = {}

            data[projector][size] = subitem
    return data


def clean(data):
    sizes = np.fromiter(data.keys(), dtype=np.int64)
    runs = np.array([x["kind"] for x in data.values()])
    return sizes, runs


import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Evaluate Performance Data")
parser.add_argument("path", type=Path, help="Path to csv")
parser.add_argument("dim", type=int, help="Dimension of the problem")
parser.add_argument(
    "--violinplot", action=argparse.BooleanOptionalAction, help="Show violin plot"
)
parser.add_argument(
    "--lineplot", action=argparse.BooleanOptionalAction, help="Create line plot"
)
parser.add_argument(
    "--show",
    default=False,
    action="store_true",
    help="Show plot",
)

group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--backward", action="store_true", help="Consider only backward projection"
)
group.add_argument(
    "--forward",
    action="store_true",
    help="Consider only forward projection",
)

args = parser.parse_args()

# Taken from https://davidmathlogic.com/colorblind/
# The IBM style
colors = {
    "Blob": {"main": "#DC267F", "complement": "#648FFF"},
    "BSpline": {"main": "#648FFF", "complement": "#DC267F"},
    "Siddon": {"main": "#785EF0", "complement": "#FE6100"},
    "Joseph": {"main": "#FE6100", "complement": "#785EF0"},
}


def speedup(data):
    siddon = data["Siddon"]["mean"]
    slowdowns = {}
    for proj, stats in data.items():
        slowdown = np.mean(np.divide(siddon, stats["mean"]))
        slowdowns[proj] = 1 / slowdown

    return slowdowns


def plot_violing(ax, sizes, runs, proj):
    idx = np.argsort(sizes)
    sizes = np.flip(sizes[idx[::-1]])
    runs = np.flip(runs[idx[::-1]], axis=0)

    if sizes.shape[0] == 8:
        sizes = sizes[[0, 4, 5, 7]]
        runs = runs[[0, 4, 5, 7], :]

    x = np.arange(0, sizes.shape[0])
    plot = ax.violinplot(runs.T, showmedians=False, showextrema=False, positions=x)

    col = colors[proj]["main"]

    # Style the body
    for pc in plot["bodies"]:
        pc.set_facecolor(col)
        pc.set_edgecolor(col)

    plot = ax.boxplot(
        runs.T,
        positions=x,
        widths=0.1,
        patch_artist=True,
        boxprops=dict(color=col, facecolor=col),
        whiskerprops=dict(color=col, linewidth=1),
        flierprops=dict(marker="o", markeredgecolor=col),
        medianprops=dict(color="w", linewidth=3),
        capprops=dict(color=col, linewidth=1),
    )
    for cap in plot["caps"]:
        cap.set_xdata(cap.get_xdata() + np.array([-0.05, 0.05]))

    ax.set_xlabel("Phantom size", labelpad=10)
    ax.set_ylabel("Time (sec)", labelpad=10)
    ax.set_yscale("log", base=2)

    ax.set_xticks(x, sizes)


def lineplot(ax, sizes, runs, proj):
    mean = np.mean(runs, axis=1)
    stddev = np.std(runs, axis=1)

    c = colors[proj]["main"]
    plot = ax.plot(sizes, mean, linestyle="None", marker="o", color=c)
    alpha = 0.15

    ax.plot(sizes, mean, linestyle="-", label=proj, color=c)
    lower = mean - stddev
    upper = mean + stddev
    ax.plot(sizes, lower, alpha=alpha, linestyle="--", color=c)
    ax.plot(sizes, upper, alpha=alpha, linestyle="--", color=c)
    ax.fill_between(sizes, lower, upper, alpha=alpha, color=c)

    ax.set_ylabel("Time (sec)")
    ax.set_xlabel("Phantom Size")
    plt.legend(loc="upper left")

    return mean, stddev


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    clrs = sns.color_palette("husl", 5)

    from scipy import interpolate

    path = args.path
    dim = args.dim

    projection_kind = "forward"
    if args.forward:
        projection_kind = "forward"
    elif args.backward:
        projection_kind = "backward"

    data = read_csv(path, projection_kind)

    import numpy as np

    sns.set_style("whitegrid")

    fig, axes = None, None
    if args.lineplot:
        fig, axes = plt.subplots(figsize=(10, 10))

    stats = {}
    for i, (proj, s) in enumerate(data.items()):
        sizes = np.fromiter(s.keys(), dtype=np.int64)
        runs = np.array([x["data"] for x in s.values()])
        if args.violinplot:
            fig, axes = plt.subplots(figsize=(10, 10))
            plot_violing(axes, sizes, runs, proj)

            name = f"plot_{dim}d_violin_{projection_kind}_{proj}.png"
            plt.savefig(name, bbox_inches="tight", pad_inches=0)

        elif args.lineplot:
            idx = np.argsort(sizes)
            sizes = np.flip(sizes[idx[::-1]])
            runs = np.flip(runs[idx[::-1]], axis=0)
            mean, stddev = lineplot(axes, sizes, runs, proj)
            axes.set_xscale("log", base=2)
            axes.set_yscale("log", base=2)

            stats[proj] = {
                "sizes": sizes,
                "mean": mean,
                "stddev": stddev,
            }

    # Write lineplot only once at the end
    if args.lineplot:
        name = f"plot_{dim}d_line_{projection_kind}.png"
        plt.savefig(name, bbox_inches="tight", pad_inches=0)

        # Also calculate speedup/slowdown
        slowdowns = speedup(stats)
        import csv

        with open(f"speedup_{dim}d.csv", "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(["Siddon", "Joseph", "B-Spline", "Blob"])
            writer.writerow(
                [
                    f"{slowdowns['Siddon']:.3}",
                    f"{slowdowns['Joseph']:.3}",
                    f"{slowdowns['BSpline']:.3}",
                    f"{slowdowns['Blob']:.3}",
                ]
            )

    if args.show:
        plt.show()
