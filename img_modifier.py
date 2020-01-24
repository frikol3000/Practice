import getopt
import sys
import logging

from img_modifier import img_helper

logger = logging.getLogger()


def init():
    args = sys.argv[1:]

    if len(args) == 0:
        raise ValueError("-p can't be empty")

    opts, rem = getopt.getopt(args, "p:", ["rotate=", "resize=", "color_filter=", "flip_top", "flip_left"])
    rotate_angle = resize = color_filter = flip_top = flip_left = None

    path = None
    for opt, arg in opts:
        if opt == "-p":
            path = arg
        elif opt == "--rotate":
            rotate_angle = int(arg)
        elif opt == "--resize":
            resize = arg
        elif opt == "--color_filter":
            color_filter = arg
        elif opt == "--flip_top":
            flip_top = True
        elif opt == "--flip_left":
            flip_left = arg

    if not path:
        raise ValueError("No path")

    img = img_helper.get_img(path)
    if rotate_angle:
        img = img_helper.rotate(img, rotate_angle)

    if resize:
        w, h = map(int, resize.split(','))
        img = img_helper.resize(img, w, h)

    if color_filter:
        img = img_helper.color_filter(img, color_filter)

    if flip_left:
        img = img_helper.flip_left(img)

    if flip_top:
        img = img_helper.flip_top(img)


if __name__ == "__main__":
    init()
