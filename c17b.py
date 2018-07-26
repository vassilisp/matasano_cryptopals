from c17 import encrypt, decrypt

from tools import getBlocks, getRandom, fixed_xor, findBlockSize

from random import randint
from math import ceil
import string

from utils import *

def randomOracleModification(prev, current):
	rnd = getRandom(i)
	prev = prev[:-i] + rnd
	return prev


def getConsecutivePrev(inList, index):
	return inList[index - 1], inList[index]

def oracleAttack(cipher, oracle, bS=16):
	"""Decrypt all blocks"""

	nBlocks = ceil(len(cipher) / bS)
	res = b''
	for i in range(nBlocks):
		if len(cipher) < 2*bS:
			break
		res = decryptLastBlock(cipher, oracle, bS) + res
		cipher = cipher[:-bS]
	return res


def decryptLastBlock(cipher, oracle, bS):
	"""Decrypt full block"""

	iknown = b''
	result = b''
	for i in range(bS):
		res, iknown = findIBlock(cipher, iknown, oracle, bS)
		result = res + result

	assert len(result) == bS
	return result


def findIBlock(cipher, iknown, oracle, bS):
	"""Decrypt I byte in block
	requires intermediate known state up to I byte"""

	bS2 = 2 * bS
	cn1 = cipher[-bS2:-bS]
	cn = cipher[-bS:]

	rI = len(iknown) + 1

	mknown = fixed_xor(iknown, bytes([rI]) * (rI - 1))
	results = []
	for i in range(256):
		insert = bytes([i]) + mknown
		mm = cn1[:-len(insert)] + insert

		attempt = cipher[:-bS2]
		assert cipher == attempt + cn1 + cn
		attempt += mm + cn

		#print("ATTEMPT", i)
		if oracle(attempt):

			inter = rI ^ i
			pp = inter ^ cn1[-rI]
			results.append([bytes([pp]), bytes([inter]) + iknown, mm != cn1])


	if len(results) == 1:
		#print("Only one result")
		return results[0][0], results[0][1]

	if len(results) > 1:
		for res in results:
			if res[2]:
				return res[0], res[1]

	raise Exception("padding oracle did not work")


def test_challenge_17():
	for i in range(20):
		cipher = encrypt()
		res = oracleAttack(cipher, decrypt)
		print(res)
		if int(res[:6]) < 20:
			ass(True, "challenge 16 oracle")


if __name__ == "__main__":
	test_challenge_17()


				






	



