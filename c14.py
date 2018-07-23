
from c7 import encrypt as ecb_encrypt
from c9 import pad, unpad
from c11 import randomPad, getRandom, repetitions
from c12 import findBlockSize, detectECB, findAll

from random import randint
from base64 import b64decode

from utils import assert_equals, asq

key = None
randomPad = None

def encryption_oracle(bin_input):
	global key
	global randomPad
	if key == None:
		key = getRandom(16)
	if randomPad == None:
		randomPad = getRandom(randint(1,16))

	bin_input += appText

	padded = pad(randomPad + bin_input, 16)
	return ecb_encrypt(key, padded)


def getBlocks(binInput, blockSize):
	return [binInput[i: i + blockSize] for i in range(0, len(binInput), blockSize)]

def findRandomSize(oracle):
	bS = findBlockSize(oracle)
	res = 0
	for i in range(bS*3):
		enc = oracle(b'A'*i)
		if findRepeated(enc, bS) != -1:
			print("I", i)
			inputInBlock = i - 2 * bS
			res = bS - inputInBlock
			break
	return res

def findRepeated(binInput, blockSize):
	"""first repeated blocks"""
	blocks = getBlocks(binInput, blockSize)
	res = -1
	for i in range(len(blocks) - 1):
		if blocks[i] == blocks[i+1]:
			res = i
			break
	return res

class OracleWrapper:
	rS = 0
	bS = 0
	oracle = None
	def __init__(self, oracle):
		self.rS = findRandomSize(oracle)
		self.bS = findBlockSize(oracle)
		self.oracle = oracle

	def getOracle(self):
		return self.modified_oracle

	def modified_oracle(self, binInput):
		firstBlockInput = (self.bS - self.rS) * b'A'

		return self.oracle(firstBlockInput + binInput)[self.bS:]
		
		

def test_challenge14():

	ow = OracleWrapper(encryption_oracle)
	woracle = ow.getOracle()

	if not detectECB(woracle):
		return False
	blockSize = findBlockSize(woracle)
	print("Block size:", blockSize)

	res = findAll(woracle)
	print("RESULT", res)
	assert_equals(res, appText, 'Challenge 14 decryption')

appText = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")

if __name__ == "__main__":
	assert_equals = asq

	enc = encryption_oracle(b'hello')
	bs = findBlockSize(encryption_oracle)
	print(bs)
	getBlocks(enc, bs)
	rs = findRandomSize(encryption_oracle)
	print('actual random size:',len(randomPad),  ",calculated random size:", rs)
	test_challenge14()


