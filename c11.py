from c10 import cbc_encrypt
from c7 import encrypt as ecb_encrypt
from c9 import pad
from c6 import hamming_keys

from os import urandom
from random import randint
import itertools

def getRandomL(klen):
	return urandom(klen)

def getRandom(klen):
	return urandom(klen)

def randomPad(bin_input):
	return getRandom(randint(5, 10)) + bin_input + getRandom(randint(5,10))

def encryption_oracle(bin_input):
	if type(bin_input) is not bytes:
		bin_input = bin_input.encode()

	key = getRandom(16)

	padded = randomPad(bin_input)

	if randint(0,1):
		print("ECB encrypt")
		padded = pad(padded, 16)
		out = ecb_encrypt(key, padded)
	else:
		print("CBC encrypt")
		iv = getRandom(16)
		out = cbc_encrypt(iv, key, padded)
	return out


def repetitions(bin_input, size):
	blocks = [bin_input[i: i+size] for i in range(0, len(bin_input), size)]
	if len(blocks[-1]) < size: blocks = blocks[:-1]
	scr = sum([1 if pair[0] == pair[1] else 0 for pair in itertools.combinations(blocks, 2)])
	#print(scr)
	return scr

def guess():
	text = b"YELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW sub"
	ciphert = encryption_oracle(text)
	
	scr = hamming_keys(ciphert, 16, 0)
	print("SCORE is", scr)
	res = 'CBC'
	#if scr<2000:
	if repetitions(ciphert, 4) > 0:
		res = 'ECB'
	print("ALGO is", res)

if __name__ == "__main__":
	guess()

