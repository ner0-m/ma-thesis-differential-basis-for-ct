# from PIL import Image, ImageDraw
#
# width = 640
# height = 640
#
# gridsize = 10
# padding = 100
# pixelside = (640 - 2 * padding) / gridsize
#
# image = Image.new(mode='L', size=(width, height), color=255)
# draw = ImageDraw.Draw(image)
#
# draw.rectangle((padding, padding, width - padding, height - padding))
# draw.line((50, 375, 600, 175))
#
# for i in range(gridsize):
#     for j in range(gridsize):
#         x = padding + i * pixelside
#         y = padding + j * pixelside
#         draw.rectangle((x, y, x + pixelside, y + pixelside))
#
# image.show()

import cairo
import math

width = 1024
height = 1024


def define_line(cr, src, dest):
    cr.move_to(src[0], src[1])
    cr.line_to(dest[0], dest[1])


def draw_line(cr, src, dest, stroke_width=0.0025, color=(0, 0, 0)):
    cr.move_to(src[0], src[1])
    cr.line_to(dest[0], dest[1])

    # set color
    cr.set_source_rgb(color[0], color[1], color[2])
    # set stroke
    cr.set_line_width(stroke_width)
    # draw it
    cr.stroke()


def draw_circle(cr, start, radius, stroke_width=0.0025, color=(0, 0, 0)):
    cr.arc(start[0], start[1], radius, 0, 2 * math.pi)

    # set color
    cr.set_source_rgb(color[0], color[1], color[2])
    cr.fill()


def fill_grid_cell(cr, p, gridsize, color):
    startx = p[0] / gridsize[0]
    starty = p[1] / gridsize[1]
    recwidth = 1 / gridsize[0]
    recheight = 1 / gridsize[1]

    # create rectangle
    cr.rectangle(startx, starty, recwidth, recheight)

    # set color
    cr.set_source_rgba(color[0], color[1], color[2], color[3] or 1)

    # fill background
    cr.fill()


def draw_grid(cr, rows, cols, start=0.1, end=0.9, stroke_width=0.0025, color=(0, 0, 0)):
    # draw rows
    for i in range(1, rows - 1):
        define_line(cr, (start, i / rows), (end, i / rows))

    # draw cols
    for i in range(1, cols - 1):
        define_line(cr, (i / cols, start), (i / cols, end))

    # set color
    cr.set_source_rgb(color[0], color[1], color[2])
    cr.set_line_width(stroke_width)
    cr.stroke()

    # draw cols
    for i in range(1, cols - 1):
        define_line(cr, (i / cols + 0.05, start - 0.05), (i / cols + 0.05, end + 0.05))

    cr.set_source_rgb(color[0] + 0.3, color[1] + 0.3, color[2] + 0.3)
    cr.set_line_width(stroke_width / 2)
    cr.stroke()

def main():
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    cr.scale(width, height)

    # create centered rectangle
    # cr.rectangle(0, 0, width, height)
    cr.rectangle(0, 0, 1, 1)

    # set color to white
    cr.set_source_rgb(1, 1, 1)

    # fill background
    cr.fill()

    # set color to white
    cr.set_source_rgb(1, 1, 1)

    # create centered rectangle
    cr.rectangle(0.1, 0.1, 0.8, 0.8)

    # preserve inside color
    cr.fill_preserve()

    # set color to black
    cr.set_source_rgb(0, 0, 0)

    # set line width
    cr.set_line_width(0.0025)

    # draw stroke
    cr.stroke()

    # draw grid
    # draw_grid(cr, 10, 10)

    # 0.478, 0.635, 0.968
    cur_x = 1
    cur_y = 3
    fill_grid_cell(cr, (cur_x, cur_y - 1), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y + 1), (10, 10), (0.478, 0.635, 0.968, 0.5))

    cur_x += 1
    cur_y = 3
    fill_grid_cell(cr, (cur_x, cur_y - 1), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y + 1), (10, 10), (0.478, 0.635, 0.968, 0.5))

    cur_x += 1
    cur_y = 2
    fill_grid_cell(cr, (cur_x, cur_y - 1), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y + 1), (10, 10), (0.478, 0.635, 0.968, 0.5))

    cur_x += 1
    fill_grid_cell(cr, (cur_x, cur_y - 1), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y + 1), (10, 10), (0.478, 0.635, 0.968, 0.5))

    cur_x += 1
    fill_grid_cell(cr, (cur_x, cur_y - 1), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y + 1), (10, 10), (0.478, 0.635, 0.968, 0.5))

    cur_x += 1
    fill_grid_cell(cr, (cur_x, cur_y - 1), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y + 1), (10, 10), (0.478, 0.635, 0.968, 0.5))

    cur_x += 1
    cur_y = 1
    fill_grid_cell(cr, (cur_x, cur_y), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y + 1), (10, 10), (0.478, 0.635, 0.968, 0.5))

    cur_x += 1
    cur_y = 1
    fill_grid_cell(cr, (cur_x, cur_y), (10, 10), (0.478, 0.635, 0.968, 0.5))
    fill_grid_cell(cr, (cur_x, cur_y + 1), (10, 10), (0.478, 0.635, 0.968, 0.5))

    # draw grid
    draw_grid(cr, 10, 10)

    # draw ray
    draw_line(cr, (0.05, 0.35), (0.95, 0.15))

    ims.write_to_png("image.png")


if __name__ == "__main__":
    main()
