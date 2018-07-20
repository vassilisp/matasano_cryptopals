import binascii
import base64
import itertools

from utils import asq
from nose.tools import assert_equals

def hamming(byte_input1, byte_input2):
	"""Calculate the Hamming distance between two bytearrays/strings"""
	if type(byte_input1) is not bytes:
		byte_input1 = byte_input1.encode()
		byte_input2 = byte_input2.encode()

	assert len(byte_input1) == len(byte_input2)
	return sum(bin(b1^b2).count('1') for b1, b2 in zip(byte_input1, byte_input2))

#def hamming_bitstr(s1, s2):
#	"""Calculate the Hamming distance between two bit strings"""
#	assert len(s1) == len(s2)
#	return sum(c1 != c2 for c1, c2 in zip(s1, s2))
#
#def hamming_str(str1, str2):
#	bit1 = str_to_bit(str1)
#	bit2 = str_to_bit(str2)
#	return hamming_bitstr(bit1, bit2)
#	
#
#def str_to_bit(in_str):
#	byte_str = in_str.encode()
#	res_str = ""
#	for single_byte in byte_str:
#		bits = "{0:b}".format(single_byte)
#		bits = bits.rjust(8, '0')
#		res_str +=  bits
#	return res_str

#========================================
def hamming_keys(bin_input, size, Ncomb=10):
	blocks = [bin_input[i : i+size] for i in range(0, len(bin_input), size)]

	scr = 0
	if Ncomb != 0:
		blocks = blocks[:Ncomb]
	for comb in itertools.combinations(blocks,2):
		scr += hamming(comb[0], comb[1])

	return scr 
#========================================
def read_b64_file_old(filename):
	with open(filename) as f:
		encoded = str.join('', f)
		encoded = encoded.replace('\n', '')

	return base64.b64decode(encoded)

def read_b64_file(filename):
	with open(filename) as f:
		return base64.b64decode(f.read())

def getKeyLengthN(bin_input, max_key_length=40, N=3):
	res = []
	for i in range(2, max_key_length):
		score = hamming_keys(encrypted, i)/i
		res.append([score, i]) 

	res.sort()
	return res[:N]

def getKeyLength(bin_input, max_key_length=40):
	return getKeyLengthN(bin_input, max_key_length, N=1)[0][1]

#========================================
def test_hamming():
	in1 = "this is a test"	
	in2 = "wokka wokka!!!"

	res = hamming(in1, in2)
	assert_equals(res, 37)
	print("hamming function test - OK")

def test_challenge6():
	#print(encrypted)

	topKeyLen = getKeyLengthN(encrypted)
	print(topKeyLen)
	keyLen = getKeyLength(encrypted)
	print(keyLen)
	#test(keyLen, 29, "challenge 6 key size")
	assert_equals(keyLen, 29, "challenge 6 key size")
#========================================

encrypted = read_b64_file('6.txt')

if __name__ == "__main__":

	assert_equals = asq

	test_hamming()
	test_challenge6()




