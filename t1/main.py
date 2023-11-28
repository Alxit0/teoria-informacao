"""
- Alexandre Silva Regalado nº2020212059
- João Maria Santos nº2022213725
- Miguel Pinto de Santos nº2022221058
"""
from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import huffmancodec as huffc

from typing import Literal, Tuple

VAR_NAME_LIST = [
	'Acceleration',
	'Cylinders',
	'Displacement',
	'Horsepower',
	'ModelYear',
	'Weight',
	'Mpg'
]

car_set_data_options = Literal['Acceleration','Cylinders','Displacement','Horsepower','ModelYear','Weight']

# ex2
def compare_mpg(matriz:np.ndarray):
	"""Compara o consumo de combustível (MPG) com várias variáveis em um conjunto de dados.

	Args:
		matriz (np.ndarray): O array NumPy contendo o conjunto de dados.
	"""
	fig, axs = plt.subplots(3, 2)

	def _config_subplot(x, y, title_data):
		# valores
		axs[x, y].plot(
			matriz[:,VAR_NAME_LIST.index(title_data)],	# data of x axis
			matriz[:,6], '.'							# data of y axis
		)

		# titulo
		axs[x, y].set_title(f'MPG vs {title_data}')
		
		# labels dos axis
		axs[x, y].set_xlabel(title_data)
		axs[x, y].set_ylabel('MPG')
		
		plt.subplots_adjust(hspace=1)
		plt.subplots_adjust(wspace=.5)

	_config_subplot(0, 0, 'Acceleration')
	_config_subplot(0, 1, 'Cylinders')
	_config_subplot(1, 0, 'Displacement')
	_config_subplot(1, 1, 'Horsepower')
	_config_subplot(2, 0, 'ModelYear')
	_config_subplot(2, 1, 'Weight')
	
	plt.show()

# ex3
def get_alfabeto(matriz:np.ndarray):
	"""Retorna o alfabeto representado por uma matriz.

	Args:
		matriz (np.ndarray): O array NumPy contendo os dados.

	Returns:
		Set[int]: Um conjunto de valores que representam o alfabeto da matriz.
	"""

	# pede para converter
	convertido = matriz.astype(np.uint16)
	
	# nums from 0 to 65535
	return np.asarray(range(2**16))

# ex4
def num_ocurrencias(vals:np.ndarray):
	"""Conta o número de ocorrências de valores em um array.

	Args:
		vals (np.ndarray): O array NumPy contendo os valores.

	Returns:
		Dict: Um dicionário com os valores como chaves e o número de ocorrências como valores.
	"""

	d = {}

	for i in vals:
		if not i in d:
			d[i] = 0

		d[i] += 1

	return d

# ex5
def grafico_barras(histograma:dict, name:str):
	"""Gera um gráfico de barras a partir de um histograma.

	Args:
		histograma (Dict): Um dicionário no formato 'any: int'.
		name (str): Nome para o gráfico.
	"""
	plt.figure()

	# ordenar as keys (simbolos)
	x_data = [str(i) for i in sorted(histograma.keys())]
	
	# fazer com que os valores coicidam com as keys ordenadas
	y_data = [histograma[int(i)] for i in x_data]

	plt.bar(x_data, y_data, color='pink')
	plt.xticks(rotation='vertical', fontsize=7)
	
	plt.xlabel(name)
	plt.ylabel('Count')

	plt.show()

# ex6
def _mini_histogram(nums:np.ndarray, ini:int, fin:int) -> dict:
	"""Calcula um histograma para um conjunto de números dentro de um intervalo.

	Args:
		nums (np.ndarray): O array NumPy contendo os números.
		ini (int): O início do intervalo.
		fin (int): O final do intervalo.

	Returns:
		Dict[int, int]: Um dicionário com os números como chaves e suas contagens como valores.
	"""

	resp = {}

	for i in nums:
		# intervalo
		if not (ini <= i <= fin):
			continue

		if i not in resp:
			resp[i] = 0
		
		resp[i] += 1

	return resp

def binning(matriz:np.ndarray, var:car_set_data_options, *, show_graf=False):
	"""Agrupa valores em um array NumPy com base em uma variável especificada e, opcionalmente, exibe um histograma.

	Args:
		matriz (np.ndarray): O array NumPy de entrada contendo os dados a serem agrupados.
		var (Literal['Weight', 'Displacement', 'Horsepower']): A variável a ser usada para agrupamento.
		show_graf (bool, opcional): Se True, exibe um histograma dos dados agrupados. Padrão é False.

	Returns:
		np.ndarray: Um array com os valores agrupados com base na variável especificada.
	"""

	# name_of_var: (index_of_var_in_matrix, pace)
	configs = {
		'Weight': (VAR_NAME_LIST.index('Weight'), 40),
		'Displacement': (VAR_NAME_LIST.index('Displacement'), 5),
		'Horsepower': (VAR_NAME_LIST.index('Horsepower'), 5),
	}

	if var not in configs:
		return matriz[:,VAR_NAME_LIST.index(var)]
	
	n_var, pace = configs[var]

	vals = matriz[:,n_var]
	
	for i in range(0, vals.max(), pace):
		cur_hist = _mini_histogram(vals, i, i+pace-1)

		if len(cur_hist) == 0:
			continue

		# 3: 421, 5: 13
		main_value = max(cur_hist.keys(), key=lambda x:cur_hist[x])

		# substituicao
		vals[(i <= vals) & (vals <= i+pace-1)] = main_value

	if show_graf:
		main_hist = num_ocurrencias(vals)
		grafico_barras(main_hist, var)

	return vals

# ex7
def _probs(vals:np.ndarray):
	"""Calcula a probabilidade de ocorrência de valores em um array.

	Args:
		vals (np.ndarray): Um array NumPy contendo valores.

	Returns:
		Dict[int, float]: Um dicionário com os valores como chaves e suas probabilidades como valores.
	"""

	contagem = num_ocurrencias(vals)
	probs = {i:j/len(vals) for i, j in contagem.items()}

	return probs

def entropia(matriz:np.ndarray, var:car_set_data_options) -> float:
	"""Calcula a entropia de um conjunto de dados com base em uma variável específica.

	Args:
		matriz (np.ndarray): O array NumPy contendo o conjunto de dados.
		var (car_set_data_options): A variável a ser usada para calcular a entropia.

	Returns:
		float: O valor da entropia calculada.
	"""
	
	# obter valores binados
	new_vals = binning(matriz, var)
	
	# probs = lista de valores (not keys) do dicionario de _probs
	probs = np.asarray(list(_probs(new_vals).values()))

	# ent = - ∑ p(x) * log2(p(x))
	valor_entropia = - np.sum(probs*np.log2(probs))

	return valor_entropia

# ex8
def huffman_bits_por_sybol(matriz:np.ndarray, var: car_set_data_options) -> Tuple[float, float]:
	"""Calcula a média e a variância do número de bits por símbolo usando a codificação Huffman.

	Args:
		matriz (np.ndarray): O array NumPy contendo o conjunto de dados.
		var (car_set_data_options): A variável a ser usada para a codificação Huffman.

	Returns:
		Tuple[float, float]: Um tuple contendo a média e a variância do número de bits por símbolo.
	"""

	# obter valores binados
	new_vals = binning(matriz, var)

	codec = huffc.HuffmanCodec.from_data(new_vals)
	symbols, lenghts = codec.get_code_len()

	# probabilidades de cada simbolo
	probs = _probs(new_vals)


	# li -> lenght ('a': 01 -> li=2| 'b':0101 -> li=4)
	# si -> symbol ('a' | 'b')

	# avg = ∑ li * p(si)
	media_bits = sum([
		li*probs[si]
		for li, si in zip(lenghts, symbols)
	])

	# var = ∑ (avg - li)^2 * p(si)
	variancia = sum([
		(media_bits-li)**2 * probs[si]
		for li, si in zip(lenghts, symbols) 
	])

	return media_bits, variancia

# ex9
def pearson_correlation(matriz:np.ndarray, var: car_set_data_options):
	"""Calcula a correlação de Pearson entre duas variáveis em um conjunto de dados.

	Args:
		matriz (np.ndarray): O array NumPy contendo o conjunto de dados.
		var (car_set_data_options): A variável com a qual deseja calcular a correlação.

	Returns:
		float: O valor da correlação de Pearson entre 'Mpg' e a variável especificada.
	"""

	# lista com os valores do Mpg
	mpg = matriz[:,VAR_NAME_LIST.index('Mpg')]

	# lista com os valores do spec passado
	other_coef = matriz[:,VAR_NAME_LIST.index(var)]

	return np.corrcoef(mpg, other_coef)[0, 1]

# ex10
def _histograma_2d(vals1: np.ndarray, vals2: np.ndarray) -> np.ndarray:
	"""Calcula o histograma 2D de dois conjuntos de valores.

	Args:
		vals1 (np.ndarray): O primeiro conjunto de valores.
		vals2 (np.ndarray): O segundo conjunto de valores.

	Returns:
		np.ndarray: Um array NumPy representando o histograma 2D.
	"""

	resp = np.zeros((vals1.max()+1, vals2.max()+1))

	for i, j in zip(vals1, vals2):
		resp[i][j] += 1
	
	return resp

def mutal_information(matriz:np.ndarray, var: car_set_data_options):
	"""Calcula a informação mútua entre duas variáveis em um conjunto de dados.

	Args:
		matriz (np.ndarray): O array NumPy contendo o conjunto de dados.
		var (car_set_data_options): A variável com a qual deseja calcular a informação mútua.

	Returns:
		float: O valor da informação mútua entre 'Mpg' e a variável especificada.
	"""

	vals1 = matriz[:,VAR_NAME_LIST.index('Mpg')]
	vals2 = binning(matriz, var)

	# Calcula o histograma 2D dos vals
	hist = _histograma_2d(vals1, vals2)

	# Normaliza o histograma
	hist = hist / np.sum(hist)

	# Calcula as probabilidades marginais
	p_x = np.sum(hist, axis=1)
	p_y = np.sum(hist, axis=0)

	# Inicializa a informação mútua
	mi = 0.0

	# Calcula a informação mútua usando a fórmula
	# Σ Σ p(x, y) * log2(p(x, y) / (p(x) * p(y)))
	for i in range(len(p_x)):
		for j in range(len(p_y)):
			if hist[i, j] > 0:
				mi += hist[i, j] * np.log(hist[i, j] / (p_x[i] * p_y[j]))


	return mi

# ex11
def _get_binned_matriz(matriz:np.ndarray):
	"""Retorna uma matriz com valores binados com base nas variáveis.

	Args:
		matriz (np.ndarray): O array NumPy contendo o conjunto de dados.

	Returns:
		np.ndarray: Uma matriz com valores binados.
	"""

	resp_matriz = np.zeros(matriz.shape)

	for i in range(len(matriz[0])):
		resp_matriz[:,i] = binning(matriz, VAR_NAME_LIST[i])
	
	return resp_matriz

def _get_MImin_MImax(matriz:np.ndarray):
	"""Retorna as variáveis com os valores mínimos e máximos de informação mútua.

	Args:
		matriz (np.ndarray): O array NumPy contendo o conjunto de dados.

	Returns:
		Tuple[str, str]: Um tuple com o nome da variável com a menor e a maior informação mútua.
	"""

	temp = []

	for i in VAR_NAME_LIST[:-1]:
		val = mutal_information(matriz, i)
		temp.append((i, val))

	mimin = min(temp, key=lambda x:x[1])[0]
	mimax = max(temp, key=lambda x:x[1])[0]

	return mimin, mimax

def mpg_predict(matriz:np.ndarray, num_of_cars:int, *, use_binning=True, rm_MImin=False, rm_MImax=False):
	"""Prevê o consumo de combustível (mpg) para um conjunto de carros.

	Args:
		matriz (np.ndarray): O array NumPy contendo o conjunto de dados.
		num_of_cars (int): O número de carros para os quais deseja fazer a previsão.
		use_binning (bool, opcional): Se True, utiliza valores binados. Padrão é True.
		rm_MImin (bool, opcional): Se True, remove a variável com informação mútua mínima. Padrão é False.
		rm_MImax (bool, opcional): Se True, remove a variável com informação mútua máxima. Padrão é False.

	Returns:
		np.ndarray: Um array com as previsões de consumo de combustível para os carros especificados.
	"""

	# escolher caso queremos usar o binning ou nao
	if use_binning:
		usable_matriz = _get_binned_matriz(matriz)
	else:
		usable_matriz = matriz

	# obter o spec com MI(mutual information) min e max
	MImin, MImax = _get_MImin_MImax(matriz)

	# inicializar matriz de resposta
	resp_matrix = np.zeros((num_of_cars,))

	# inicializar lista com os 'pesos' para a multiplicacao dos valores
	mult_matrix = np.asarray([-0.146, -0.4909, +0.0026, -0.0045, +0.6725, -0.0059, 0])

	# caso queiramos remover um spec apenas temos de alterar
	# o valor correspndente da matriz de mult para 0 pois 0 * spec = 0 (removido)
	if rm_MImin:
		mult_matrix[VAR_NAME_LIST.index(MImin)] = 0
	
	if rm_MImax:
		mult_matrix[VAR_NAME_LIST.index(MImax)] = 0

	# iterar pelos carros e calcular o MPG
	for i in range(num_of_cars):
		mpg_pred2 = -5.5241 + np.sum(np.multiply(usable_matriz[i],mult_matrix))
		resp_matrix[i] = round(mpg_pred2)
	
	return resp_matrix

def graf_mpgs(matriz:np.ndarray):
	"""Gera um gráfico de consumo de combustível (mpg) para diferentes cenários.

	Args:
		matriz (np.ndarray): O array NumPy contendo o conjunto de dados.
	"""

	x_axis = range(len(matriz))
	
	ver = matriz[:,6]
	full = mpg_predict(matriz, len(matriz))
	not_MImin = mpg_predict(matriz, len(matriz), rm_MImin=True)
	not_MImax = mpg_predict(matriz, len(matriz), rm_MImax=True)
	

	# plot grafico
	plt.figure(figsize=(10, 6))
	plt.plot(x_axis, ver, color='black', label='ver')
	plt.plot(x_axis, full, color='g', label='full')
	plt.plot(x_axis, not_MImin, color='r', label='not_MImin')
	plt.plot(x_axis, not_MImax, color='b', label='not_MImax')

	# por legenda
	plt.legend()

	plt.show()


def main():
	# ex1
	path_of_data = './CarDataset.xlsx'
	data = pd.read_excel(path_of_data) 	# a)
	
	matriz = data.to_numpy()	# b)
	var_names = data.columns.values.tolist()	# c)

	def ex2():
		compare_mpg(matriz)	

	def ex3():
		print(get_alfabeto(matriz))

	def ex4():
		spec: car_set_data_options = 'Cylinders'
		hist = num_ocurrencias(matriz[:,VAR_NAME_LIST.index(spec)])
		print(spec)
		pprint(hist)

	def ex5():
		spec: car_set_data_options = 'Acceleration'
		for spec in VAR_NAME_LIST:
			grafico_barras(num_ocurrencias(matriz[:,VAR_NAME_LIST.index(spec)]), spec)

	def ex6():
		binning(matriz, 'Weight', show_graf=True)

	def ex7():
		print(f"{'spec':^15}|{'entropia':^22}")
		print('-'*35)
		for i in VAR_NAME_LIST[:-1]:
			print(f"{i:14} | {str(entropia(matriz, i)):20}")

	def ex8():
		print(f"{'spec':^15}|{'media_bits':^22}|{'variancia':^15}")
		print('-'*58)
		for i in VAR_NAME_LIST[:-1]:
			media_bits, variancia = huffman_bits_por_sybol(matriz, i)
			print(f'{i:14} | {str(media_bits):20} | {str(variancia):14}')

	def ex9():
		for var_to_pearson in VAR_NAME_LIST[:-1]:
			pe_cor = pearson_correlation(matriz, var_to_pearson)
			a = f"PeCor('{var_to_pearson}')"
			print(f"{a:21} {pe_cor}")

	def ex10():
		for i in VAR_NAME_LIST[:-1]:
			print(f"MI of {i:15}", mutal_information(matriz, i))

	def ex11():
		# print(mpg_predict(matriz, len(matriz)))
		graf_mpgs(matriz)

	ex2()
	ex3()
	ex4()
	ex5()
	ex6()
	ex7()
	ex8()
	ex9()
	ex10()
	ex11()
	

if __name__ == '__main__':
	main()
