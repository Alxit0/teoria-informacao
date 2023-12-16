from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING
from huffmantree import HuffmanTree

if TYPE_CHECKING:
	from gzip_1 import GZIP


CODE_LENGHTS_ORDER = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]

# tabela1 Doc2 - pag 10
EXTRA_BITS_LENGTHS = [
	(0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
	(1, 11), (1, 13), (1, 15), (1, 17),
	(2, 19), (2, 23), (2, 27), (2, 31),
	(3, 35), (3, 43), (3, 51), (3, 59),
	(4, 67), (4, 83), (4, 99), (4, 115),
	(5, 131), (5, 163), (5, 195), (5, 227),
	(0, 258)
]

# tabela2 Doc2 - pag 10
EXTRA_BITS_DIST = [
	(0, 1), (0, 2), (0, 3), (0, 4),
	(1, 5), (1, 7),
	(2, 9), (2, 13),
	(3, 17), (3, 25),
	(4, 33), (4, 49),
	(5, 65), (5, 97),
	(6, 129), (6, 193),
	(7, 257), (7, 385),
	(8, 513), (8, 769),
	(9, 1025), (9, 1537),
	(10, 2049), (10, 3073),
	(11, 4097), (11, 6145),
	(12, 8193), (12, 12289),
	(13, 16385), (13, 24577)
]


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
def _get_next_index(gzip: GZIP, hft: HuffmanTree) -> int:
	hft.resetCurNode()
	cur_node = -1

	while cur_node < 0:
		direction = gzip.readBits(1)
		cur_node = hft.nextNode(str(direction))
	
	return cur_node

def read_hufftree_lens(gzip: GZIP, hft: HuffmanTree, num_of_vals: int) -> List[int]:
	"""_summary_

	Returns:
		List[int]: _description_
	"""

	resp = []
	while len(resp) < num_of_vals:
		indice = _get_next_index(gzip, hft)
		
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

# ex7
def decompress_lz77(gzip: GZIP, output:List[int], hft_lit_len:HuffmanTree, hft_dist:HuffmanTree, verbose=False) -> List[int]:
	"""Descompactação dos dados comprimidos, com base nos códigos de Huffman e no algoritmo LZ77

	Args:
		gzip (GZIP): gzip para descomprimir
		output (List[int]): lista de codigos
		hft_lit_len (HuffmanTree): huffman tree dos literais/tamanhos (lits/lengths)
		hft_dist (HuffmanTree): huffman tree das distancias

	Returns:
		List[int]: lista dos valores utf8 dos simbolos descomprimidos
	"""


	while True:

		code_lit_len = _get_next_index(gzip, hft_lit_len)

		# If the code reached is 256, its the end and we terminate the loop
		if code_lit_len == 256:
			break

		# If the code reached is in the interval [0, 256[,
		# just append the value read corresponding a the literal to the output array
		elif code_lit_len < 256:
			output.append(code_lit_len)

		# If the code reached is in the interval [257, 285],
		# it is refering to the length of the string to copy
		elif code_lit_len > 256:
			
			# calculate length
			readExtra, length = EXTRA_BITS_LENGTHS[code_lit_len - 257]
			length += gzip.readBits(readExtra)

			# calculate distance
			code_dist = _get_next_index(gzip, hft_dist)
			readExtra, distance = EXTRA_BITS_DIST[code_dist]
			distance += gzip.readBits(readExtra)

			# For each one of the range(length) iterations,
			# copy the character at index len(output)-distance to the end of the output array
			for _ in range(length):
				output.append(output[-distance])

	if verbose:
		print(*map(chr, output), sep='')

	return output
