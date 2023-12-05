from __future__ import annotations
from typing import Dict, List, Tuple, TYPE_CHECKING
from huffmantree import HuffmanTree, HFNode

if TYPE_CHECKING:
	from gzip_1 import GZIP


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


def storeCLENLengths(self, HCLEN):
	'''Stores the code lengths for the code lengths alphabet in an array'''

	# CLENcodeLens[idx] = N translates to: "the code for idx in the code lengths alphabet has a length of N"
	# if N == 0, that indexes' code length is not used

	CLENcodeLens = [0] * 19
	for i in range(HCLEN+4):
		CLENcodeLens[CODE_LENGHTS_ORDER[i]] = self.readBits(3)
	
	return CLENcodeLens

def createHuffmanFromLens(self, lenArray: List[int], verbose=False):
	'''Takes an array with symbols' Huffman codes' lengths and returns
	a formated Huffman tree with said codes

	If verbose==True, it prints the codes as they're added to the tree'''

	htr = HuffmanTree()
	# max_len is the code with the largest length 
	max_len = max(lenArray)
	# max_symbol é o maior símbolo a codificar
	max_symbol = len(lenArray)
	
	# retirar contagem dos diferentes comprimentos dos codigos
	bl_count = []
	for i in range(max_len+1):
		bl_count.append(lenArray.count(i))
	bl_count[0] = 0

	# Get first code of each code length 
	code = 0
	next_code = [0 for i in range(max_len+1)]
	for bits in range(1, max_len+1):
		code = (code + bl_count[bits-1]) << 1
		next_code[bits] = code
	

	# Define codes for each symbol in lexicographical order
	for n in range(max_symbol):
		# Length associated with symbol n 
		length = lenArray[n]
		if(length != 0):
			code = bin(next_code[length])[2:]
			# In case there are 0s at the start of the code, we have to add them manualy
			# length-len(code) 0s have to be added
			extension = "0"*(length-len(code)) 
			htr.addNode(extension + code, n, verbose)
			next_code[length] += 1
	
	return htr;

def storeTreeCodeLens(self, size, CLENTree):
	'''Takes the code lengths huffmantree and stores the code lengths accordingly'''

	# Array where the code lengths will be stored 
	treeCodeLens = [] 

	while (len(treeCodeLens) < size):
		# Sets the current node to the root of the tree
		CLENTree.resetCurNode()
		found = False

		# While reading, if a leaf hasn't been found, keep searching bit by bit
		while(not found):
			curBit = self.readBits(1)
			code = CLENTree.nextNode(str(curBit))
			if(code != -1 and code != -2):
				found = True

		# SPECIAL CHARACTERS
		# 18 - Reads 7 extra bits 
		# 17 - Reads 3 extra bits
		# 16 - Reads 2 extra bits
		if(code == 18):
			ammount = self.readBits(7)
			# According to the 7 bits just read, set the following 11-139 values on the length array to 0 
			treeCodeLens += [0]*(11 + ammount)
		if(code == 17):
			ammount = self.readBits(3)
			# According to the 3 bits just read, set the following 3-11 values on the length array to 0 
			treeCodeLens += [0]*(3 + ammount)
		if(code == 16):
			ammount = self.readBits(2)
			# According to the 2 bits just read, set the following 3-6 values on the length array to the latest length read
			treeCodeLens += [prevCode]*(3 + ammount)
		elif(code >= 0 and code <= 15):
			# If a special character isn't found, just set the next code length to the value found
			treeCodeLens += [code]
			prevCode = code

	return treeCodeLens
