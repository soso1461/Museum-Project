from mcpi.minecraft import Minecraft
from PIL import Image


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
			
			
def find_best_match(r, g, b):
	best_match_id = -128
	best_diff = (1 << 31) - 1
	
	for index, material in enumerate(material_list):
		color = material[4]
		diff = sum(map(lambda x: x ** 2, (color[0] - r, color[1] - g, color[2] - b)))

		if diff < best_diff:
			best_match_id = index
			best_diff = diff
	return best_match_id
	

def load_materials():
	base_path = '/home/rpi4/Material.txt'
	
	with open(base_path, 'r', encoding='utf-8') as reader:
		materials = reader.readlines()
		
		for material in materials:
			token = material.rstrip().split(',')
			
			material_list.append([token[0], int(token[1]), int(token[2]), token[3], tuple(map(int, token[4:]))])
		
	
def clear_blocks(mc, width, height):
	mc.setBlocks(0, 0, 0, width - 1, 64, height - 1, 0)
	mc.setBlocks(0, -1, 0, width - 1, -1, height - 1, 35, 0)


def print_blocks(mc, block_ids):
	for block in block_ids:
		mc.setBlock(block[0], -1, block[1], 35, block_ids[block])
		
		
def create_mcpi_image(img_path):
	load_materials()
	block_ids = convert_mcpi_blocks(img_path)
	
	mc = Minecraft.create()
	
	clear_blocks(mc, 128, 128)
	print_blocks(mc, block_ids)
			

def main():
	img_path = '/home/rpi4/stable-image/test-128x128.jpg'
	create_mcpi_image(img_path)
	

if __name__ == '__main__':
	main()
