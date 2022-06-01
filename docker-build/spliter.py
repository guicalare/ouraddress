from os.path import exists as file_exists
from tqdm import tqdm

with open("callejero_españa.csv", "r", encoding='iso8859-1') as f:
	input_file_data = f.readlines()

cabecera = input_file_data[0]


for linea in tqdm(input_file_data[1:]):

	id = linea.split("#")[1]

	if file_exists(f"{id}"):
		with open(f"{id}", "a", encoding='iso8859-1') as f:
			f.write(linea)
	else:
		with open(f"{id}", "w", encoding='iso8859-1') as f:
			f.write(cabecera)