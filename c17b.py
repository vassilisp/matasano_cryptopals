from c17 import encrypt, decrypt

from tools import getBlocks, getRandom, fixed_xor

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

def oracleAttack():
	"""Decrypt all blocks"""
	bS = 16
	cipher = encrypt()

	nBlocks = ceil(len(cipher) / bS)
	res = b''
	for i in range(nBlocks):
		if len(cipher) < 2*bS:
			break
		res = decryptLastBlock(cipher) + res
		cipher = cipher[:-bS]
	return res



def decryptLastBlock(cipher):
	"""Decrypt full block"""

	bS = 16

	iknown = b''
	result = b''
	for i in range(bS):
		res, iknown = findIBlock(cipher, iknown)
		result = res + result

	assert len(result) == bS
	return result


def findIBlock(cipher, iknown = ''):
	"""Decrypt I byte in block
	requires intermediate known state up to I byte"""

	bS = 16
	bS2 = 2 * bS
	cn1 = cipher[-bS2:-bS]
	cn = cipher[-bS:]

	rI = len(iknown) + 1
	I = bS - rI

	mknown = fixed_xor(iknown, bytes([rI]) * (rI - 1))
	results = []
	for i in range(256):
		insert = bytes([i]) + mknown
		mm = cn1[:-len(insert)] + insert

		attempt = cipher[:-bS2]
		assert cipher == attempt + cn1 + cn
		attempt += mm + cn

		#print("ATTEMPT", i)
		if decrypt(attempt):

			mp = bytes([rI]) * rI
			inter = fixed_xor(mp, mm[-rI:])
			inter2 = rI ^ mm[-rI]

			pp = inter[0] ^ cn1[-rI]
			pp = bytes([pp])
			results.append([pp, inter])

	if len(results) == 1:
		#print("Only one result")
		return results[0][0], results[0][1]

	if len(results) > 1:
		for res in results:
			if (res[0] != bytes([rI])):
				#print("Found by comparing to rI")
				return res[0], res[1]
			if (res[0].decode() in string.printable):
				#print("Found printable")
				return res[0], res[1]

	raise Exception("padding oracle did not work-adding dummy")


def test_challenge_17():
	for i in range(20):
		res = oracleAttack()
		print(res)
		if int(res[:6]) < 20:
			ass(True, "challenge 16 oracle")


if __name__ == "__main__":
	test_challenge_17()


				






	



