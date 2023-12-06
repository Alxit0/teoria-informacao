from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING
from huffmantree import HuffmanTree

if TYPE_CHECKING:
	from gzip_1 import GZIP


CODE_LENGHTS_ORDER = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]

# ex1
def read_hs_values(gzip: GZIP, verbose: bool = False) -> Tuple[int, int, int]:
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

# ex2
def read_clen_lens(gzip: GZIP, HCLEN: int) -> List[int]:
	"""Stores the code lengths for the code lengths alphabet in an array

	Returns:
		List[int]: code lengths
	"""
	
	comprimentos_dos_codigos = [0] * 19
	for i in range(HCLEN+4):
		comprimentos_dos_codigos[CODE_LENGHTS_ORDER[i]] = gzip.readBits(3)
	
	return comprimentos_dos_codigos

# ex3
def create_huftree_from_lens(comprimentos_dos_codigos: List[int], verbose=False) -> HuffmanTree:
	"""Takes an array with symbols 'Huffman codes' lengths and returns
	a formated Huffman tree with said codes
	
	Returns:
		HuffmanTree: huffman tree of codes
	"""

	max_len = max(comprimentos_dos_codigos)
	
	# calcular a contagem dos diferentes comprimentos dos codigos
	bl_count = [0] * (max_len+1)
	for i in comprimentos_dos_codigos:
		bl_count[i] += 1
	bl_count[0] = 0

	# calcular o primeiro codigo para cada comprimento
	code = 0
	next_code = [0 for i in range(max_len+1)]
	for bits in range(1, max_len+1):
		code = (code + bl_count[bits-1]) << 1
		next_code[bits] = code
	
	# criar a arvore de huffman
	htr = HuffmanTree()
	for i, lenght in enumerate(comprimentos_dos_codigos):
		if lenght == 0:
			continue

		code = bin(next_code[lenght])[2:].zfill(lenght)
		htr.addNode(code, i, verbose)
		next_code[lenght] += 1
	
	return htr

# ex4, ex5
def read_hufftree_lens(gzip: GZIP, hft: HuffmanTree, num_of_vals: int) -> List[int]:
	"""_summary_

	Returns:
		List[int]: _description_
	"""
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
	while len(resp) < num_of_vals:
		indice = next_indice()
		
		if indice == 16:
			# copy the previous code length 3 - 6 times (2 bits of length)
			resp.extend([resp[-1]] * (gzip.readBits(2)+3))

		elif indice == 17:
			# repeat a code length of 0 for 3 - 10 times (3 bits of length)
			resp.extend([0] * (gzip.readBits(3)+3))

		elif indice == 18:
			# repeat a code length of 0 for 11 - 138 times (7 bits of length)
			resp.extend([0] * (gzip.readBits(7)+11))

		else:
			resp.append(indice)
	
	return resp
