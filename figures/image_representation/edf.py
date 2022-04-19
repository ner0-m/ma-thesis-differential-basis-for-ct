import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.transforms import Bbox
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg

from scipy.ndimage import gaussian_filter


def readedf(filename, from_elsa=True):
    # Issue 1: The 4th dimensions is read as (3,0,1,2)
    try:
        f = open(filename, "r", encoding="utf8", errors="ignore")
        content = f.read()
    except:
        print("failed opening " + filename)
        return
    if content[0] != "{":
        print("Failed reading opening header marker")
        f.close()

    header = content[content.find("{") + 1 : content.find("}")]
    header_split = header.split()
    header_dict = dict()
    header_length = len(header_split)

    for i in range(int(header_length / 3)):
        header_dict[header_split[i * 3]] = header_split[i * 3 + 2].strip(";")
    DATATYPES = {
        "UnsignedByte": np.uint8,
        "UnsignedShort": np.uint16,
        "SignedInteger": np.uint32,
        "UnsignedInteger": np.uint32,
        "UnsignedInt": np.uint32,
        "UnsignedLong": np.uint32,
        "Float": np.float32,
        "FloatValue": np.float32,
        "Real": np.float32,
        "DoubleValue": np.float64,
    }
    header_dict["DataType"] = DATATYPES[header_dict["DataType"]]
    header_dict["Image"] = int(header_dict["Image"])
    nrOfDimensions = 0
    header_dict["Dim_1"] = int(header_dict["Dim_1"])
    nrOfDimensions = 1
    if "Dim_2" in header_dict:
        header_dict["Dim_2"] = int(header_dict["Dim_2"])
        nrOfDimensions = 2
    else:
        header_dict["Dim_2"] = 1
    if "Dim_3" in header_dict:
        header_dict["Dim_3"] = int(header_dict["Dim_3"])
        nrOfDimensions = 3
    else:
        header_dict["Dim_3"] = 1
    if "Dim_4" in header_dict:
        header_dict["Dim_4"] = int(header_dict["Dim_4"])
        nrOfDimensions = 4
    else:
        header_dict["Dim_4"] = 1
    header_dict["Size"] = int(header_dict["Size"])

    f.seek(len(header) + 3)
    data = np.fromfile(f, dtype=header_dict["DataType"])

    if nrOfDimensions == 4:
        data = data.reshape(
            header_dict["Dim_1"],
            header_dict["Dim_2"],
            header_dict["Dim_3"],
            header_dict["Dim_4"],
        )

    if nrOfDimensions == 2:
        if from_elsa:
            data = data.reshape(header_dict["Dim_2"], header_dict["Dim_1"])
        else:
            data = data.reshape(header_dict["Dim_1"], header_dict["Dim_2"])

    if nrOfDimensions == 3:
        data = data.reshape(
            header_dict["Dim_1"], header_dict["Dim_2"], header_dict["Dim_3"]
        )

    data = np.squeeze(data)
    f.close()
    return data


def writeedf(data, filename):
    try:
        f = open(filename, "wb")
    except:
        print("failed opening " + filename)
        return

    header = dict()
    header["HeaderID"] = "EH:000001:000000:000000"
    header["Image"] = str(1)
    header["ByteOrder"] = "LowByteFirst"
    header["DataType"] = "DoubleValue"
    header["Dim_1"] = str(data.shape[0])
    if len(data.shape) == 1:
        header["Dim_1"] = str(1)
        header["Dim_2"] = str(data.shape[0])
        data = np.expand_dims(data, axis=0)
    if len(data.shape) >= 2:
        header["Dim_2"] = str(data.shape[1])
    if len(data.shape) >= 3:
        header["Dim_3"] = str(data.shape[2])
    if len(data.shape) == 4:
        header["Dim_4"] = str(data.shape[3])
    header["Size"] = str(np.prod(data.shape) * 8)
    header["Date"] = datetime.datetime.now().strftime("%d-%b-%Y")
    spacingArray = [1] * len(data.shape)
    header["Spacing"] = " ".join(str(elem) for elem in spacingArray)

    f.write("{\n".encode())

    for key in header:
        s = key + " = " + header[key] + ";\n"
        f.write(s.encode())

    for i in range(f.tell(), 1021):
        f.write(" ".encode())

    f.write("\n}\n".encode())

    data.astype("float64").tofile(f)

    f.close()

    return


def imshow3dfull(img, fig=None):

    global data, data_tmp, v_min, v_max
    v_min = np.amin(img)
    v_max = np.amax(img)
    data = img
    data_tmp = data

    shape = data.shape
    if fig is None:
        fig, ax = plt.subplots()
    else:
        ax = plt.axes()
        # ax = fig.axes[0]
    plt.subplots_adjust(left=0.25, bottom=0.25)
    img_artist = ax.imshow(
        data[:, :, int(shape[2] / 2)],
        interpolation="none",
        cmap="gray",
        vmin=v_min,
        vmax=v_max,
    )
    fig.colorbar(img_artist)

    axlevel = plt.axes([0.25, 0.15, 0.65, 0.03])
    slevel = Slider(axlevel, "Slice", 0, 0.9999, valinit=0.5, valstep=0.0001)

    def update_level(val):
        img_artist.set_data(data[:, :, int(slevel.val * data.shape[2])])
        fig.canvas.blit(ax.bbox)

    slevel.on_changed(update_level)

    rax = plt.axes([0.025, 0.5, 0.15, 0.15])
    radio = RadioButtons(rax, ("xy", "yz", "xz"), active=0)

    def update_view(label):
        global data_tmp
        global data
        if label == "xy":
            data = np.transpose(data_tmp, (0, 1, 2))
        if label == "yz":
            data = np.transpose(data_tmp, (1, 2, 0))
        if label == "xz":
            data = np.transpose(data_tmp, (2, 0, 1))
        img_artist.set_data(data[:, :, int(slevel.val)])
        fig.canvas.blit(ax.bbox)

    radio.on_clicked(update_view)

    axmin = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    axmax = fig.add_axes([0.25, 0.05, 0.65, 0.03])

    smin = Slider(axmin, "Min", np.amin(img), np.amax(img), valinit=np.amin(img))
    smax = Slider(axmax, "Max", np.amin(img), np.amax(img), valinit=np.amax(img))

    def update_clim(val):
        global v_min
        global v_max
        img_artist.set_clim([smin.val, smax.val])
        v_min = smin.val
        v_max = smax.val
        img_artist.set_data(data[:, :, int(slevel.val)])
        fig.canvas.blit(ax.bbox)

    smin.on_changed(update_clim)
    smax.on_changed(update_clim)

    plt.show()


def imshow(img, fig=None, show_colorbar=True):
    v_min = np.amin(img)
    v_max = np.amax(img)

    if fig is None:
        fig, ax = plt.subplots()
    else:
        ax = plt.axes()
        # ax = fig.axes[0]
    img_artist = ax.imshow(
        img, interpolation="none", cmap="gray", vmin=v_min, vmax=v_max
    )
    if show_colorbar:
        fig.colorbar(img_artist)
    fig.canvas.draw()
    plt.show()


def savepng(img, output_file):
    v_min = np.amin(img)
    v_max = np.amax(img)

    fig, ax = plt.subplots()
    img_artist = ax.imshow(
        img, interpolation="none", cmap="gray", vmin=v_min, vmax=v_max
    )
    fig.canvas.draw()
    plt.axis("off")
    plt.savefig(output_file, bbox_inches="tight", pad_inches=0)
