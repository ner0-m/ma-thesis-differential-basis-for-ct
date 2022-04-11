# With a lot of help from https://gist.github.com/AllanHasegawa/9d73beda100a360b3008
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches
import math
import random


class Ray:
    def __init__(self):
        self.origin = np.zeros((2))
        self.direction = np.zeros((2))

    def norm(self):
        self.direction = self.direction / np.linalg.norm(self.direction)

    def plot(self, axes, t_min, t_max, color=(0, 0, 0), zorder=10):
        x0 = self.origin[0] + t_min * self.direction[0]
        y0 = self.origin[1] + t_min * self.direction[1]
        d0 = self.direction[0] * (t_max - t_min)
        d1 = self.direction[1] * (t_max - t_min)
        axes.quiver(
            x0,
            y0,
            d0,
            d1,
            angles="xy",
            scale_units="xy",
            scale=1,
            width=0.005,
            zorder=zorder,
            color="#F7768E",
        )


class AABB:
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def intersects(self, ray):
        r_t_min = 0
        r_t_max = 0
        t_min = 0
        t_max = 0
        ty_min = 0
        ty_max = 0

        size = self.high - self.low

        bounds_x1 = self.low[0]
        bounds_x2 = self.low[0]
        bounds_y1 = self.low[1]
        bounds_y2 = self.low[1]
        irayd = 1.0 / ray.direction
        if irayd[0] >= 0:
            bounds_x2 += size[0]
        else:
            bounds_x1 += size[0]
        if irayd[1] >= 0:
            bounds_y2 += size[1]
        else:
            bounds_y1 += size[1]

        t_min = (bounds_x1 - ray.origin[0]) * irayd[0]
        t_max = (bounds_x2 - ray.origin[0]) * irayd[0]
        ty_min = (bounds_y1 - ray.origin[1]) * irayd[1]
        ty_max = (bounds_y2 - ray.origin[1]) * irayd[1]

        t_min = max(t_min, ty_min)
        t_max = min(t_max, ty_max)

        if (t_min < t_max) and (t_max > 0):
            r_t_min = t_min
            r_t_max = t_max
            return (True, r_t_min, r_t_max)
        return (False, -1, -1)


class Grid:
    def __init__(self, aabb):
        self.width = aabb.high[0] - aabb.low[0]
        self.height = aabb.high[1] - aabb.low[1]
        self.grid = np.zeros((self.width + 1, self.height + 1))
        self.aabb = aabb

    def plot(self, axes):
        for ix in range(self.aabb.low[0], self.aabb.high[0]):
            for iy in range(self.aabb.low[1], self.aabb.high[1]):
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
                patch = patches.PathPatch(path, facecolor="white", lw=1)
                axes.add_patch(patch)


# Find the distance between "frac(s)" and "1" if ds > 0, or "0" if ds < 0.
def diff_distance(s, ds):
    if s < 0:
        s = s - int(-1 + s)
    else:
        s = s - int(s)
    if ds > 0:
        return (1.0 - s) / ds
    else:
        ds = -ds
        return s / ds


class AmanatidesTraversal:
    def __init__(self, grid, ray):
        self.grid = grid
        self.ray = Ray()
        self.ray.origin = ray.origin.copy()
        self.ray.direction = ray.direction.copy()
        if self.ray.direction[0] == 0:
            self.ray.direction[0] = sys.float_info.min
        if self.ray.direction[1] == 0:
            self.ray.direction[1] = sys.float_info.min
        self.t_min = 0

    def initialize(self):
        (cube_result, cube_hit_t_min, cube_hit_t_max) = self.grid.aabb.intersects(
            self.ray
        )
        if cube_result:
            cube_hit_point = self.ray.origin + (cube_hit_t_min) * self.ray.direction
            self.t_min = cube_hit_t_min
            self.cube_hit_t_min = cube_hit_t_min

            print("DDA: Cube Hit Point:", cube_hit_point)

            self.step_x = math.copysign(1.0, self.ray.direction[0])
            self.step_y = math.copysign(1.0, self.ray.direction[1])

            self.t_delta_x = self.step_x / self.ray.direction[0]
            self.t_delta_y = self.step_y / self.ray.direction[1]

            self.t_max_x = diff_distance(cube_hit_point[0], self.ray.direction[0])
            self.t_max_y = diff_distance(cube_hit_point[1], self.ray.direction[1])

            if cube_hit_point[0] < 0:
                cube_hit_point[0] -= 1
            if cube_hit_point[1] < 0:
                cube_hit_point[1] -= 1
            self.voxel = np.array(cube_hit_point, dtype=int)
            """
            this conditional solves the problem where the "cube_hit_point" is just
            outside the grid because of floating point imprecision.
            """
            while (
                self.voxel[0] < self.grid.aabb.low[0]
                or self.voxel[1] < self.grid.aabb.low[1]
                or self.voxel[0] >= self.grid.aabb.high[0]
                or self.voxel[1] >= self.grid.aabb.high[1]
            ):
                print("DDA: Skyping:", self.voxel)
                if not self.step():
                    return False

            return True
        else:
            return False

    def step(self):
        self.t_min = min(self.t_max_x, self.t_max_y) + self.cube_hit_t_min
        if self.t_max_x < self.t_max_y:
            self.t_max_x += self.t_delta_x
            self.voxel[0] += self.step_x
            if (
                self.voxel[0] >= self.grid.aabb.high[0]
                or self.voxel[0] < self.grid.aabb.low[0]
            ):
                return False
        else:
            self.t_max_y += self.t_delta_y
            self.voxel[1] += self.step_y
            if (
                self.voxel[1] >= self.grid.aabb.high[1]
                or self.voxel[1] < self.grid.aabb.low[1]
            ):
                return False
        return True

    def get_voxel(self):
        return self.voxel.copy()

    def get_t_interval(self):
        # transform to unit space again
        return (self.t_min, (min(self.t_max_x, self.t_max_y) + self.cube_hit_t_min))


class Voxel:
    def __init__(self, grid):
        self.grid = grid

    def plot(self, axes, x, y, color="#4682B4", weight=None, zorder=3):
        low_x = x
        low_y = y
        high_x = x + 1
        high_y = y + 1
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
        patch = patches.PathPatch(
            path, facecolor=color, edgecolor="k", lw=1, zorder=zorder
        )

        if weight:
            rx, ry = low_x, low_y
            cx = rx + 0.5
            cy = ry + 0.5
            axes.annotate(
                f"{weight:.3}",
                (cx, cy),
                color="w",
                weight="bold",
                fontsize=9,
                ha="center",
                va="center",
            )
        axes.add_patch(patch)


fig, axes = plt.subplots(1, 1, figsize=(10, 10))

ray = Ray()
# ray.origin = np.array([-7.65,3.27])
ray.origin = np.array([-1, 1])
ray.direction = np.array([1.0, 0.345])
ray.norm()

gridaabb = AABB(np.array([0, 0]), np.array([6, 6]))
grid = Grid(gridaabb)
# print("Grid N. Quadrants: (", grid.width, ",", grid.height, ")")
grid.plot(axes)
traversal = AmanatidesTraversal(grid, ray)

tmin = traversal.t_min
voxel = Voxel(grid)

points = []
voxels = []
weights = []
if traversal.initialize():
    cube_hit = ray.origin + traversal.get_t_interval()[0] * ray.direction
    points.append(cube_hit)

    prev_t = traversal.t_min
    while True:
        # Ignore while t_max is negative.
        if traversal.get_t_interval()[1] < 0:
            if not traversal.step():
                break
            continue

        # current position
        points.append(ray.origin + traversal.get_t_interval()[1] * ray.direction)

        # Save current position
        cur_voxel = traversal.get_voxel()
        voxels.append(cur_voxel)

        # Move forward
        do_next_step = traversal.step()

        # Now calculate the distance
        dist = traversal.t_min - prev_t
        weights.append(dist)

        # Save last t value
        prev_t = traversal.t_min

        # break if necessary
        if not do_next_step:
            break


def get_projected(p1, p2, p3):
    l2 = np.sum((p1 - p2) ** 2)
    t = np.sum((p3 - p1) * (p2 - p1)) / l2
    return p1 + t * (p2 - p1)


def slice_traversal_clean():
    # Print ray going through the volume
    ray.plot(axes, tmin, traversal.get_t_interval()[1], zorder=3)
    cleaned = []
    for v in voxels:
        if not contains(cleaned, lambda x: x[0] == v[0]):
            cleaned.append(v)

    import numpy as np

    p1 = points[0]
    p2 = points[-1]
    for v in cleaned:
        # Voxel fill
        voxel.plot(axes, v[0], v[1], zorder=1)
        voxel.plot(axes, v[0], v[1] + 1, color="#bfd4e6", zorder=1)
        voxel.plot(axes, v[0], v[1] - 1, color="#bfd4e6", zorder=1)

    v = cleaned[2]
    for offset in [-0.5, 0.5, 1.5]:
        p = np.array([v[0] + 0.5, v[1] + offset])

        # Plot Voxel centers
        axes.plot(p[0], p[1], "ok", ms=5, zorder=5)

        projection = get_projected(p1, p2, p)

        # Plot projection distance line
        axes.plot([projection[0], p[0]], [projection[1], p[1]], ":k", zorder=2)

        # Plot circle
        axes.add_patch(plt.Circle(p, 1, fill=False))


def slice_traversal():
    # Print ray going through the volume
    ray.plot(axes, tmin, traversal.get_t_interval()[1], zorder=3)
    cleaned = []
    for v in voxels:
        if not contains(cleaned, lambda x: x[0] == v[0]):
            cleaned.append(v)

    import numpy as np

    p1 = points[0]
    p2 = points[-1]
    for v in cleaned:
        for offset in [-0.5, 0.5, 1.5]:
            p3 = np.array([v[0] + 0.5, v[1] + offset])
            projection = get_projected(p1, p2, p3)
            axes.plot([projection[0], p3[0]], [projection[1], p3[1]], ":k", zorder=2)

            # Plot Voxel centers
            axes.plot(int(v[0]) + 0.5, int(v[1]) + offset, "ok", ms=5, zorder=5)

        # Voxel fill
        voxel.plot(axes, v[0], v[1], zorder=1)
        voxel.plot(axes, v[0], v[1] + 1, color="#bfd4e6", zorder=1)
        voxel.plot(axes, v[0], v[1] - 1, color="#bfd4e6", zorder=1)


def siddons_traversal():
    # Print ray going through the volume
    ray.plot(axes, tmin, traversal.get_t_interval()[1], zorder=2)

    for v, w in zip(voxels, weights):
        voxel.plot(axes, v[0], v[1], weight=w, zorder=1)

    for p in points:
        axes.plot(p[0], p[1], "ok", ms=5, zorder=3)


def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


import argparse
import pathlib

parser = argparse.ArgumentParser(
    description="Visualize either slice or siddons traversal"
)
parser.add_argument(
    "--slice", action=argparse.BooleanOptionalAction, help="Visualize Slice traversal"
)
parser.add_argument(
    "--slice-clean", action=argparse.BooleanOptionalAction, help="Visualize Slice traversal"
)
parser.add_argument(
    "--siddon", action=argparse.BooleanOptionalAction, help="Visualize Siddon traversal"
)
parser.add_argument(
    "--show", action=argparse.BooleanOptionalAction, help="Visualize Slice traversal"
)
parser.add_argument(
    "output_dir", type=pathlib.Path, help="Path to directory to dump image in"
)

args = parser.parse_args()
output = args.output_dir

# Keep aspect ration, but don't force square
axes.set_aspect("equal", "box")

plt.axis((-1.1, 7.1, -0.1, 6.1))
plt.axis("off")
if args.slice:
    slice_traversal()
    plt.savefig(
        f"{output}/slice_traversal.png", dpi=120, bbox_inches="tight", pad_inches=0
    )
elif args.slice_clean:
    slice_traversal_clean()
    plt.savefig(
        f"{output}/slice_traversal_clean.png",
        dpi=120,
        bbox_inches="tight",
        pad_inches=0,
    )
else:
    siddons_traversal()
    plt.savefig(
        f"{output}/siddon_traversal.png", dpi=120, bbox_inches="tight", pad_inches=0
    )

if args.show:
    plt.show()
