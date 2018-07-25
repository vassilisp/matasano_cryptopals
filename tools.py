from os import urandom
import itertools

from utils import *

#functions

def fixed_xor(bin_input1, bin_input2):
	if len(bin_input1) == len(bin_input2):
		return bytes([x ^ y for x,y in zip(bin_input1, bin_input2)])


#utils
def getBlocks(binInput, blockSize):
	return [binInput[i: i + blockSize] for i in range(0, len(binInput), blockSize)]

def getRandom(klen):
	return urandom(klen)


#analysis

def findBlockSize(oracle):
	t1 = len(oracle(b''))
	t2 = t1
	i = 0
	while t2 == t1:
		t2 = len(oracle(b'A'*i))
		i += 1
	return abs(t2 - t1)

def repetitions(bin_input, size=8):
	blocks = getBlocks(bin_input, size)
	if len(blocks[-1]) < size: blocks = blocks[:-1]
	scr = sum([1 if pair[0] == pair[1] else 0 for pair in itertools.combinations(blocks, 2)])
	#print(scr)
	return scr



def test_fixed_xor_corner():
	assert_equals(fixed_xor(b'', b''), b'', 'fixed xor with empty parts')
