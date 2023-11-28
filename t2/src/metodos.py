from typing import Dict, List, Tuple
from gzip_1 import GZIP
from huffmantree import HuffmanTree, HFNode

def ex1(gzip: GZIP, verbose: bool = False) -> Tuple[int, int, int]:
	"""Método que leia o formato do bloco

	Returns:
		(int, int, int): _description_
	"""
	
	HLIT = gzip.readBits(5)
	HDIST = gzip.readBits(5)
	HCLEN = gzip.readBits(4)

	if verbose:
		print(f"{HLIT = }")
		print(f"{HDIST = }")
		print(f"{HCLEN = }")

	return HLIT, HDIST, HCLEN

def ex2(gzip: GZIP, HCLEN: int, verbose: bool = False) -> List[int]:
	"""Método que armazene num array os comprimentos dos códigos do \
		“alfabeto de comprimentos de códigos”, com base em HCLEN

	Returns:
		list: lista de comprimentos dos codigos
	"""

	comprimentos_dos_codigos = []
	for _ in range(HCLEN+4):
		comprimentos_dos_codigos.append(gzip.readBits(3))
	
	if verbose:
		print(f"{comprimentos_dos_codigos = }")


	return comprimentos_dos_codigos

def ex3(comprimentos_dos_codigos: List[int], verbose: bool = False) -> HuffmanTree:
	"""método que converta os comprimentos dos códigos da alínea \
		anterior em códigos de Huffman
	
	Returns:
		HuffmanTree: arvore de huffamn
	"""
	MAX_BITS = max(comprimentos_dos_codigos)
	
	bl_count = []
	for i in range(MAX_BITS+1):
		bl_count.append(comprimentos_dos_codigos.count(i))
	bl_count[0] = 0

	code = 0
	codigos_iniciais = []
	for bits in range(1, MAX_BITS+1):
		code = (code + bl_count[bits-1]) << 1
		codigos_iniciais.append(code)
	
	codigos_de_huffman = []
	for i, j in enumerate(bl_count):
		for k in range(j):
			codigos_de_huffman.append(bin(codigos_iniciais[i-1]+k)[2:].zfill(i))

	a = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]
	ordenado = {}
	for i, j in zip(a, comprimentos_dos_codigos):
		if j not in ordenado:
			ordenado[j] = []
		
		ordenado[j].append(i)
	
	ordenado = {i:sorted(j) for i,j in ordenado.items()}
	print(ordenado)
	
	hft = HuffmanTree()
	for i, j in enumerate(bl_count):
		for k in range(j):
			hft.addNode(bin(codigos_iniciais[i-1]+k)[2:].zfill(i), ordenado[i][k], False)

	if verbose:
		print(f"{codigos_de_huffman = }")

	return hft


def ex4_comprimentos_literais(gzip: GZIP, hft: HuffmanTree, HLIT: int):
	def next_indice():
		cur_code = ''
		while hft.findNode(cur_code) < 0:
			cur_code += str(gzip.readBits(1))
		
		return hft.findNode(cur_code)


	resp = []

	idx = 0
	while idx < HLIT + 257:
		cur = next_indice()
		print(cur)

		idx+=1


