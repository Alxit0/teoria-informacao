"""
	3/10/2021 18:23 Alexandre Regalado	"ex1 - ex4"
	10/10/2021 18:45 João Santos	"ex5 - ex6"
"""

from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from typing import Literal

# ex2
def compare_mpg(matriz:np.ndarray):
	fig, axs = plt.subplots(3, 2)

	def _config_subplot(x, y, x_data, y_data, title_data):
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
	
	convertido = matriz.astype(np.uint16)
	
	return set(range(131072))

# ex4
def num_ocurrencias(vals:np.ndarray):
	d = {}

	for i in vals:
		if not i in d:
			d[i] = 0

		d[i] += 1

	return d

# ex5
def grafico_barras(histograma:dict):
	fig = plt.figure()

	x_data = [str(i) for i in sorted(histograma.keys())]
	y_data = [histograma[int(i)] for i in x_data]

	plt.bar(x_data, y_data, color='pink')
	
	plt.show()

# ex6
def _mini_histogram(nums:np.ndarray, ini:int, fin:int) -> dict:
	resp = {}

	for i in nums:
		if not (ini <= i <= fin):
			continue

		if i not in resp:
			resp[i] = 0
		
		resp[i] += 1

	return resp

def binning(matriz:np.ndarray, var:Literal['Weight', 'Displacement', 'Horsepower']):
	configs = {
		'Weight': (5, 40),
		'Displacement': (2, 5),
		'Horsepower': (3, 5),
	}
	n_var, pace = configs[var]

	vals = matriz[:,n_var]
	
	for i in range(0, vals.max(), pace):
		cur_hist = _mini_histogram(vals, i, i+pace-1)

		if len(cur_hist) == 0:
			continue

		main_value = max(cur_hist.keys(), key=lambda x:cur_hist[x])

		for j in range(len(vals)):
			if i <= vals[j] <= i+pace-1:
				vals[j] = main_value


	main_hist = num_ocurrencias(vals)
	grafico_barras(main_hist)



def main():
	# ex 1
	path_of_data = './CarDataset.xlsx'
	data = pd.read_excel(path_of_data) 	# a)
	
	matriz = data.to_numpy()	# b)
	var_names = data.columns.values.tolist()	# c)


	# ex2
	# compare_mpg(matriz)	

	# # ex3
	# print(get_alfabeto(matriz))
	
	# # ex 4
	# hist = num_ocurrencias(matriz[:,0])
	# pprint(hist)

	# # ex5
	# grafico_barras(hist)

	# ex6
	binning(matriz, 'Weight')




if __name__ == '__main__':
	main()