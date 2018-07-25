from c17 import encrypt, decrypt

from tools import getBlocks, getRandom, fixed_xor

from random import randint
from math import ceil
import string


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
	print(res)



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

			pp = inter[0] ^ cn1[-rI:][0]
			pp = bytes([pp])
			results.append([pp, inter])

	if len(results) == 1:
		return results[0][0], results[0][1]

	if len(results) > 1:
		for res in results:
			if (res[0].decode() in string.printable) or (res[0] != bytes([rI])):
				return res[0], res[1]

	return results[0][0], results[0][1]
	print("padding oracle did not work-adding dummy")



if __name__ == "__main__":
	oracleAttack()


				






	



