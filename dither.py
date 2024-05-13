from PIL import Image


width, height = 0, 0


def index(i, j):
    global width

    return i * width + j


def apply_error(target, err, factor):
    r = int(target[0] + err[0] * factor)
    g = int(target[1] + err[1] * factor)
    b = int(target[2] + err[2] * factor)
    rgb_list = [r, g, b]

    for i in range(3):
        if rgb_list[i] < 0:
            rgb_list[i] = 0
        elif rgb_list[i] > 255:
            rgb_list[i] = 255
    return tuple(rgb_list)


def floyd_steinberg_dither(img_path):
    global width, height

    with Image.open(img_path) as im:
        mode, size = im.mode, im.size
        width, height = size[0], size[1]
        pixels = list(im.getdata())

    colors = [(0, 0, 0), (255, 255, 255)]

    for y in range(height):
        for x in range(width):
            target = pixels[index(y, x)]
            diff_list = []

            for c in colors:
                diff = sum(map(lambda z: z ** 2, (c[0] - target[0], c[0] - target[0], c[0] - target[0]))) ** .5
                diff_list.append(diff)
            if diff_list[0] < diff_list[1]:
                pixels[index(y, x)] = colors[0]
            else:
                pixels[index(y, x)] = colors[1]

            new_target = pixels[index(y, x)]
            err = (target[0] - new_target[0], target[1] - new_target[1], target[2] - new_target[2])

            if x != width - 1:
                pixels[index(y, x + 1)] = apply_error(pixels[index(y, x + 1)], err, 7 / 16)
            if y != height - 1:
                pixels[index(y + 1, x)] = apply_error(pixels[index(y + 1, x)], err, 5 / 16)
                if x > 0:
                    pixels[index(y + 1, x - 1)] = apply_error(pixels[index(y + 1, x - 1)], err, 3 / 16)
                if x != width - 1:
                    pixels[index(y + 1, x + 1)] = apply_error(pixels[index(y + 1, x + 1)], err, 1 / 16)

    new_image = Image.new(mode, size)
    new_image.putdata(pixels)

    return new_image
