import sys
from os import path

import re

def collect_pizzas(max_slices, pizza_sizes, num_needed_pizzas=-1):
	num_needed_pizzas = len(pizza_sizes) if (num_needed_pizzas == -1) \
							else num_needed_pizzas 

	temp_slices = 0
	temp_sizes = []

	for pizza_index, pizza_size in reversed(list(enumerate(pizza_sizes))):
		if (temp_slices + pizza_size) <= max_slices:
			temp_slices += pizza_size
			temp_sizes.append(pizza_index)

			if (len(temp_sizes) == num_needed_pizzas) \
					or (temp_slices == max_slices):
				break

	temp_sizes.reverse()
	return (temp_slices, temp_sizes)

def order_pizzas(input_file):
	max_slices = -1
	pizza_sizes = []

	with open(input_file) as file:
		for line in file.readlines():
			input_data = re.findall(r'\d+', line)

			if max_slices == -1:
				max_slices = int(input_data[0])
			else:
				pizza_sizes = input_data

	pizza_sizes = [ int(pizza_size) for pizza_size in pizza_sizes ]

	mean_pizza_size = sum(pizza_sizes) // len(pizza_sizes)
	num_needed_pizzas = max_slices // mean_pizza_size
	
	ordered_slices = 0
	ordered_sizes = []
	for i in range(0, -len(pizza_sizes), -1):
		cropped_sizes = pizza_sizes
		if (i < 0):
			cropped_sizes = pizza_sizes[:i]

		collected_pizzas = collect_pizzas(max_slices, cropped_sizes, 
								num_needed_pizzas)
		if (collected_pizzas[0] > ordered_slices):
			ordered_slices, ordered_sizes = collected_pizzas

	input_filename = path.splitext(path.basename(input_file))[0]
	output_file = 'output/' + input_filename + '.out'
	with open(output_file, 'w+') as file:
		num_ordered_sizes = str(len(ordered_sizes)) + '\n'
		str_ordered_sizes = ' '.join([ str(i) for i in ordered_sizes ])

		print(num_ordered_sizes, end='')
		file.write(num_ordered_sizes)

		print(str_ordered_sizes)
		file.write(str_ordered_sizes)

if __name__ == '__main__':
	try:
		order_pizzas(sys.argv[1])
	except:
		print('Error : Missing Input File Path')
		print('Usage : python ', path.basename(__file__), ' file.in')