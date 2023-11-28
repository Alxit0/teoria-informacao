from typing import Dict, List, Tuple
from gzip_1 import GZIP
from huffmantree import HuffmanTree, HFNode

CODE_LENGHTS_ORDER = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]


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
	"""Método que converta os comprimentos dos códigos da alínea \
		anterior em códigos de Huffman
	
	Returns:
		HuffmanTree: arvore de huffman
	"""
	
	# retirar contagem dos diferentes comprimentos dos codigos
	MAX_BITS = max(comprimentos_dos_codigos)
	bl_count = []
	for i in range(MAX_BITS+1):
		bl_count.append(comprimentos_dos_codigos.count(i))
	bl_count[0] = 0

	# obter os codigos iniciais para cada comprimento
	code = 0
	codigos_iniciais = []
	for bits in range(1, MAX_BITS+1):
		code = (code + bl_count[bits-1]) << 1
		codigos_iniciais.append(code)
	
	# obter todos os codigos de huffman
	ordenado: Dict[int, List[int]] = {}
	for ordem, comp in zip(CODE_LENGHTS_ORDER, comprimentos_dos_codigos):
		if comp not in ordenado:
			ordenado[comp] = []
		
		ordenado[comp].append(ordem)
	
	ordenado = {i:sorted(j) for i,j in ordenado.items()}
	
	# gerar arvore de huffman
	hft = HuffmanTree()
	for i, j in enumerate(bl_count):
		for k in range(j):
			codigo = bin(codigos_iniciais[i-1]+k)[2:].zfill(i)
			index = ordenado[i][k]
			hft.addNode(codigo, index, False)

			if verbose:
				print(f"{index:<4} {codigo}")

	return hft


def ex4(gzip: GZIP, hft: HuffmanTree, HLIT: int):
	def next_indice():
		cur_node = hft.root
		
		while cur_node is not None:
			if cur_node.left is None and cur_node.right is None:
				return cur_node.index
			
			direction = gzip.readBits(1)

			if direction == 0:
				cur_node = cur_node.left
			else:
				cur_node = cur_node.right
		
		# nao encontrou
		return -1

	resp = []
	idx = 0
	while idx < HLIT + 257:
		indice = next_indice()
		
		if indice == 16:
			# copy the previous code length 3 - 6 times (2 bits of length)
			for _ in range(gzip.readBits(2)+3):
				resp.append(resp[-1])
				idx += 1

		elif indice == 17:
			# repeat a code length of 0 for 3 - 10 times (3 bits of length)
			for _ in range(gzip.readBits(3)+3):
				resp.append(0)
				idx += 1

		elif indice == 18:
			# repeat a code length of 0 for 11 - 138 times (7 bits of length)
			for _ in range(gzip.readBits(7)+11):
				resp.append(0)
				idx += 1

		else:
			resp.append(indice)
			idx+=1
	
	return resp


