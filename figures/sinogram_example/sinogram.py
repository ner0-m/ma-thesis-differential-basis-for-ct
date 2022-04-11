import numpy as np
import matplotlib.pyplot as plt

from skimage.transform import radon, iradon

# from skimage.data import shepp_logan_phantom
# image = shepp_logan_phantom()


image = np.zeros((500, 500))
image[200:300, 200:300] = 1
# image[128, 436] = 1
# image[127, 436] = 1
# image[128, 435] = 1
# image[127, 435] = 1
#
# image[228, 176] = 1
# image[227, 176] = 1
# image[228, 175] = 1
# image[227, 175] = 1

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 4.5))
ax1.set_title("Original")
ax1.imshow(image, cmap=plt.cm.Greys_r)

# theta = np.linspace(0., 180., max(image.shape), endpoint=False)
numangles = 450
theta = np.linspace(0.0, 180.0, numangles, endpoint=False)
sinogram = radon(image, theta=theta)
dx, dy = 0.5 * 180.0 / max(image.shape), 0.5 / sinogram.shape[0]
ax2.set_title("Radon transform\n(Sinogram)")
ax2.set_xlabel("Projection angle (deg)")
ax2.set_ylabel("Projection position (pixels)")
ax2.imshow(
    sinogram,
    cmap=plt.cm.Greys_r,
    extent=(-dx, 180.0 + dx, -dy, sinogram.shape[0] + dy),
    aspect="auto",
)

reconstruction_fbp = iradon(sinogram, theta=theta, filter_name='ramp')
ax3.set_title("Reconstruction\nFiltered back projection")
ax3.imshow(reconstruction_fbp, cmap=plt.cm.Greys_r)

fig.tight_layout()
plt.show()
