"""
	Last update: 3/10/2021 18:23 Alex R.
"""

from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ex2
def compare_mpg(matriz:np.ndarray):
	fig, axs = plt.subplots(3, 2)

	def _config_subplot(axs, x, y, x_data, y_data, title_data):
		axs[x, y].plot(x_data, y_data, '.')
		axs[x, y].set_title(f'MPG vs {title_data}')
		
		axs[x, y].set_xlabel(title_data)
		axs[x, y].set_ylabel('MPG')
		
		plt.subplots_adjust(hspace=1)
		plt.subplots_adjust(wspace=.5)

	_config_subplot(0, 0, matriz[:,0], matriz[:,6], 'Acceleration')
	_config_subplot(0, 1, matriz[:,1], matriz[:,6], 'Cylinders')
	_config_subplot(1, 0, matriz[:,2], matriz[:,6], 'Displacement')
	_config_subplot(1, 1, matriz[:,3], matriz[:,6], 'Horsepower')
	_config_subplot(2, 0, matriz[:,4], matriz[:,6], 'ModelYear')
	_config_subplot(2, 1, matriz[:,5], matriz[:,6], 'Weight')
	
	plt.show()

# ex3
def get_alfabeto(matriz:np.ndarray):
	return set(matriz.astype(np.uint16).flat)

# ex4
def num_ocurrencias(matriz:np.ndarray, n_var:int):
	d = {}

	for i in matriz[:,n_var]:
		if not i in d:
			d[i] = 0

		d[i] += 1

	return d


def main():
	path_of_data = './CarDataset.xlsx'

	data = pd.read_excel(path_of_data)
	
	matriz = data.to_numpy()
	var_names = data.columns.values.tolist()

	# compare_mpg(matriz)
	# print(get_alfabeto(matriz))
	pprint(num_ocurrencias(matriz, 1))

if __name__ == '__main__':
	main()