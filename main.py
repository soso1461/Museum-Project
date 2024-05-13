from PIL import Image, ImageDraw

import os


material_list = []


def convert_mcpi_blocks(base_path):
    img = Image.open(base_path)
    px = img.load()
    material_dict = {}

    for x in range(img.width):
        for y in range(img.height):
            pixel = px[x, y]
            material_dict[(x, y)] = find_best_match(pixel[0], pixel[1], pixel[2])
    return material_dict


# FOR TEST!!!
def create_mcpi_image(block_ids, width, height):
    base_path = './texture'
    background = Image.new(mode='RGB', size=(width << 4, height << 4))
    block_textures = []

    for wool in material_list:
        block_textures.append(Image.open(os.path.join(base_path, wool[3])))

    for block_pos in block_ids:
        background.paste(block_textures[block_ids[block_pos]], (block_pos[0]*16, block_pos[1]*16))
    background.save('output.png')


def find_best_match(r, g, b):
    best_match_id = -128
    best_diff = (1 << 31) - 1

    for index, material in enumerate(material_list):
        color = material[4]
        diff = abs(color[0] - r) ** 2 + abs(color[1] - g) ** 2 + abs(color[2] - b) ** 2

        if diff < best_diff:
            best_match_id = index
            best_diff = diff
    return best_match_id


def load_materials():
    base_path = 'Material.txt'

    with open(base_path, 'r', encoding='utf-8') as reader:
        materials = reader.readlines()

        for material in materials:
            token = material.rstrip().split(',')

            material_list.append([token[0], int(token[1]), int(token[2]), token[3], tuple(map(int, token[4:]))])


def main():
    img_path = './test2.jpg'
    load_materials()
    create_mcpi_image(convert_mcpi_blocks(img_path), 64, 64)


if __name__ == '__main__':
    main()
