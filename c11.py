from c10 import cbc_encrypt
from c7 import encrypt as ecb_encrypt
from c9 import pad
from c6 import hamming_keys

from os import urandom
from random import randint

from utils import *
from tools import getRandom, repetitions

def randomPad(bin_input):
	return getRandom(randint(5, 10)) + bin_input + getRandom(randint(5,10))

def encryption_oracle(bin_input):
	if type(bin_input) is not bytes:
		try:
			bin_input = bin_input.encode()
		except:
			pass

	key = getRandom(16)

	padded = randomPad(bin_input)

	algo = "ECB"
	if randint(0,1):
		padded = pad(padded, 16)
		out = ecb_encrypt(key, padded)
	else:
		algo = "CBC"
		iv = getRandom(16)
		padded = pad(padded, 16)
		out = cbc_encrypt(iv, key, padded)
	#print(algo, "encrypt")
	return out, algo

def guess(ciphert):
	scr = hamming_keys(ciphert, 16, 0)/len(ciphert)
	rep = repetitions(ciphert, 4)
	#print("SCORE is", scr, "REPs are", rep)
	res = 'CBC'
	if rep > 0:
		res = 'ECB'
	#print("ALGO is", res)
	return res


def test_challenge11():
	text = b"YELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW submarineYELLOW sub"
	for i in range(100):
		ciphert, algo = encryption_oracle(text)
		assert_equals(guess(ciphert), algo, "Challenge 11, guess:" + str(i))
	print("Challenge 11 PASSED")

if __name__ == "__main__":
	assert_equals = asq
	test_challenge11()

