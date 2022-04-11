def set_size(width, fraction=1):
    # Width of figure (in pts)
    fig_width_pt = width * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**0.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio

    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim


class Grid:
    def __init__(self, high):
        self.low = np.array([0, 0])
        self.high = high

        width = self.high[0] - self.low[0]
        height = self.high[1] - self.low[1]

        self.grid = np.zeros((width + 1, height + 1))

    def plot(self, axes):
        for ix in range(self.low[0], self.high[0]):
            for iy in range(self.low[1], self.high[1]):
                low_x = ix
                low_y = iy
                high_x = ix + 1
                high_y = iy + 1
                verts = [
                    (low_x, low_y),  # left, bottom
                    (low_x, high_y),  # left, top
                    (high_x, high_y),  # right, top
                    (high_x, low_y),  # right, bottom
                    (0.0, 0.0),  # ignored
                ]

                codes = [
                    Path.MOVETO,
                    Path.LINETO,
                    Path.LINETO,
                    Path.LINETO,
                    Path.CLOSEPOLY,
                ]

                path = Path(verts, codes)
                # color="#4682B4"
                color = "w"
                zorder = 1
                patch = patches.PathPatch(
                    path, facecolor=color, edgecolor="k", lw=1, zorder=zorder
                )
                axes.add_patch(patch)


class Image:
    def __init__(self, high):
        self.low = np.array([0, 0])
        self.high = high

        self.grid = Grid(high)

    def plot(self, axes):
        self.grid.plot(axes)


import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

blue = "#4682B4"
red = "#F7768E"


class Detector:
    def __init__(self, center, dist, size, angle, resolution):
        principal_pointx = center[0] + dist
        principal_pointy = center[1]
        self.principal_point = np.array([principal_pointx, principal_pointy])

        self.transform = mpl.transforms.Affine2D().rotate_deg_around(
            center[0], center[1], angle
        )
        self.size = size
        self.angle = angle
        self.distance = dist
        self.resolution = resolution


    def plot_rays(self, axes, source):
        print(self.resolution)
        for j in range(self.resolution - 1):
            self.plot_ray_to(axes, source, j)

    def plot_ray_to(self, axes, source, j):
        transform = self.transform + axes.transData

        pp = np.copy(self.principal_point)
        pp[1] += self.size / 2
        pp[1] -= j
        tmp = pp - source

        s = self.transform.transform(source)
        axes.plot(s[0], s[1], "ok", ms=3, zorder=3)

        patch = patches.FancyArrow(source[0], source[1], tmp[0] - 0.25, tmp[1], color=red, width=0.05)
        patch.set_transform(transform)
        axes.add_patch(patch)

    def plot(self, axes):
        x = self.principal_point[0]
        y = self.principal_point[1]
        ymin = y - self.size / 2.
        ymax = y + self.size / 2.
        verts = [
            (x, ymin),  # left, bottom
            (x, ymax),  # left, top
        ]
        codes = [
            Path.MOVETO,
            Path.LINETO,
        ]

        for y in np.linspace(ymin, ymax, self.resolution):
            verts.append((x, y))
            verts.append((x - 0.2, y))
            codes.append(Path.MOVETO)
            codes.append(Path.LINETO)
        path = Path(verts, codes)

        patch = patches.PathPatch(path, edgecolor=blue, lw=3, capstyle="round")
        transform = self.transform + axes.transData
        patch.set_transform(transform)
        axes.add_patch(patch)


width = 345 * 2
fig, axes = plt.subplots(1, 1, figsize=set_size(width))
high = np.array([6, 6])

img = Image(high)
img.plot(axes)

for ix in range(0, high[0]):
    for iy in range(0, high[1]):
        cx = ix + 0.5
        cy = iy + 0.5

        text = f"$c_{{{ix + 6 * (5 - iy) + 1}}}$"
        axes.annotate(
            f"{text}",
            (cx, cy),
            color="k",
            fontsize=7,
            ha="center",
            va="center",
        )

source = (-4, 3)

# axes.plot(source[0], source[1], "ok", ms=3, zorder=3)

for angle in [0, 45, 90]:
    det = Detector((3, 3), 7, 5, angle, 6)
    det.plot(axes)
    det.plot_rays(axes, source)



axes.set_aspect("equal", "box")
plt.axis("off")
axes.set_xlim([-10, 13])
axes.set_ylim([-10, 13])
plt.savefig(f"testing_something.pgf", dpi=120, bbox_inches="tight", pad_inches=0)
plt.show()
