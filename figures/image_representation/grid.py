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
    def __init__(self, resolution, high):
        self.low = np.array([0, 0])
        self.high = high
        self.resolution = resolution

        width = self.high[0] - self.low[0]
        height = self.high[1] - self.low[1]

        self.grid = np.zeros((width + 1, height + 1))

    def plot(self, axes):
        inc = np.asarray(self.high / self.resolution, dtype=np.int64)
        for ix in range(self.low[0], self.high[0], inc[0]):
            for iy in range(self.low[1], self.high[1], inc[1]):
                low_x = ix
                low_y = iy
                high_x = ix + int(inc[0])
                high_y = iy + int(inc[1])
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
                color = "w"
                zorder = 3
                patch = patches.PathPatch(
                    path, facecolor="none", edgecolor="k", lw=1, zorder=zorder
                )
                axes.add_patch(patch)


class Image:
    def __init__(self, resolution, high):
        self.low = np.array([0, 0])
        self.high = high

        self.grid = Grid(resolution, high)

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

        patch = patches.PathPatch(path, edgecolor=blue, lw=3, capstyle="round", zorder=3)
        transform = self.transform + axes.transData
        patch.set_transform(transform)
        axes.add_patch(patch)


width = 345 * 2
fig, axes = plt.subplots(1, 1, figsize=set_size(width))
res = np.array([8, 8])

high = np.array([512, 512])
img = Image(res, high)
img.plot(axes)

inc = np.asarray(high / res, dtype=np.int64)
for ix in range(0, high[0], inc[0]):
    for iy in range(0, high[0], inc[1]):
        cx = ix + (inc[0] / 2.)
        cy = iy + (inc[1] / 2.)

        # text = f"$c_{{{ix + res[0] * ([res[1] - 1 - iy) + 1}}}$"
        x = int(ix / inc[0])
        y = res[1] - int(iy / inc[1]) - 1
        idx = np.ravel_multi_index(np.array([x, y]), res, order='F')

        text = f"$c_{{{idx + 1}}}$"
        axes.plot(cx, cy, marker="x", color="k", markersize=3)
        axes.annotate(
            f"{text}",
            (cx, cy - (inc[1] * 0.2)),
            color="k",
            fontsize=9,
            ha="center",
            va="center",
            zorder=3,
        )

source = (-4, 3)

axes.axhline(0, lw=5, zorder=5)
axes.axhline(512, lw=5, zorder=5)
axes.axvline(0, lw=5, zorder=5)
axes.axvline(512, lw=5, zorder=5)

# axes.plot(source[0], source[1], "ok", ms=3, zorder=3)

# for angle in [0, 45, 90]:
#     det = Detector((3, 3), 7, 5, angle, 6)
#     det.plot(axes)
#     det.plot_rays(axes, source)


def get_abdomen():
    import numpy as np

    import edf
    abdo = edf.readedf("abdomen_512_normalized.edf")
    # cut away the left side
    image = np.zeros_like(abdo)
    image[50:430, 50:370] = abdo[50:430, 50:370]
    return np.rot90(image)


abdomen = get_abdomen()

axes.imshow(abdomen, cmap="gray_r", zorder=1)

axes.set_aspect("equal", "box")
plt.axis("off")
axes.set_xlim([0, 512])
axes.set_ylim([0, 512])
plt.savefig(f"grid_pixel_representation.pgf", dpi=120, bbox_inches="tight", pad_inches=0)
# plt.show()
