from PIL import Image

import os


def compute_avg_color(img):
    mode = 'RGB'
    rgb_img = img.convert(mode)
    r_total, g_total, b_total = 0, 0, 0

    for x in range(rgb_img.width):
        for y in range(rgb_img.height):
            r, g, b = rgb_img.getpixel((x, y))
            r_total += r
            g_total += g
            b_total += b
    total = rgb_img.width * rgb_img.height
    r_avg = round(r_total / total)
    g_avg = round(g_total / total)
    b_avg = round(b_total / total)

    return r_avg, g_avg, b_avg


def main():
    base_path = './texture'
    textures = os.listdir(base_path)

    for texture in textures:
        if os.path.splitext(texture)[1] != '.png':
            continue
        print(texture)

        with Image.open(os.path.join(base_path, texture), 'r') as img:
            print(compute_avg_color(img))


if __name__ == '__main__':
    main()

