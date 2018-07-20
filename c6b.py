import c6
import c3
import math
import c5

from utils import *

def transpose(byte_input, window):
	full_len = len(byte_input)
	blocks = math.ceil(full_len/window)
	byteblock_array = []
	byteblocks = []
	byteblocks2 = []
	for i in range(window):
		byteblock_array.insert(1, [])
		byteblocks.insert(1, "")

	for i in range(window):
		for block in range(blocks):
			try:
				byteblock_array[i].append(byte_input[i+(block*window)])  
				#print(i, block, i+(block*window))
			except Exception as ex:
				if block != blocks-1 and (i+(block*window)) > len(byte_input):
					raise ex
				#print(i, block, "ERROR")
				continue

	for i in range(window):
		byteblocks[i] = bytes(byteblock_array[i])
	return byteblocks

def analyze(encrypted, keyLen):
	transblocks = transpose(encrypted, keyLen)

	res = []
	for i, block in enumerate(transblocks):
		res.append(c3.find_top(block)[1])

	return bytes(res)


encrypted = c6.read_b64_file('6.txt')

def test_challenge_6b():
	keyLen = c6.getKeyLength(encrypted)
	print("key length is:", keyLen)
	key = analyze(encrypted, keyLen)
	print("KEY is:", key)

	plain = c5.repeating_key_xor(encrypted, key)
	print("===== DECRYPTED =====")
	print(plain.decode())

	assert_equals(key, b'Terminator X: Bring the noise', "challenge 6 key recovery")

if __name__ == "__main__":

	assert_equals = asq
	test_challenge_6b()




