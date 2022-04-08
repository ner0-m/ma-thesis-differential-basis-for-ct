import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Read file and create plot including window bar"
)
parser.add_argument(
    "paths", type=Path, nargs="+", help="Path to edf files which slices to be ploted"
)
parser.add_argument("--slice", type=int, help="Show figure")

args = parser.parse_args()

if __name__ == "__main__":
    data = []
    proj = []
    paths = args.paths
    slice = args.slice


    import edf

    for p in paths:
        proj.append(p.stem.split("_")[1])
        data.append(edf.readedf(p))

    if not slice:
        slice = data[0].shape[0] // 2

    import matplotlib.pyplot as plt
    plt.rcParams['font.size'] = '18'

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    for d, p in zip(data, proj):
        ax.plot(d[slice, :], label=p)

    plt.legend(loc="upper right")
    plt.savefig(f"{paths[0].parents[0]}/plot_sino_differences.png", bbox_inches="tight")
    # plt.show()
