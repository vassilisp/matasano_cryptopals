from c19input import getEncryptedList
from c18 import ctr_decrypt

from tools import fixed_xor
import itertools
import string

trigrams = [b'the', b'and', b'tha', b'ent', b'ing', b'ion', b'tio', b'for', b'nde', b'has', b'nce', b'edt', b'tis', b'oft', b'sth', b'men']

cipherList = getEncryptedList()

def analysis():
	full_key = []
	maxLen = 0
	for i, c1 in enumerate(cipherList):
		if len(c1) > maxLen:
			maxLen = len(c1)

		print("working with element", i)
		full_key.extend(analyzeTrigrams(c1, cipherList))


	full_key.sort(reverse=True, key=lambda kv: kv[2])
	#print(full_key)


	key = bytearray(maxLen)
	for kv in full_key:
		start = kv[0]
		stop = kv[1]
		value = kv[3]

		for ii, aa in enumerate(range(start, stop)):
			if key[aa] == 0: 
				key[aa] = value[ii]

	print(key)
	return key

def decryptAll(key):
	for aa, cipher in enumerate(cipherList):
		res = fixed_xor(cipher, key[:len(cipher)])
		print("element",aa,"decryption:", res)
		


def analyzeTrigrams(c1, cipherList):
	full_key = []
	for tr in trigrams:
		full_key.extend(analyze_item(tr, c1, cipherList))
	return full_key

def analyze_item(trigram, c1, cipherList):
	lc = len(c1)
	tr = trigram
	lt = len(tr)

	full_key = []
	for ii in range(lc - lt):
		#print("In range", ii)
		c1part =c1[ii:ii+lt]
		gk = fixed_xor(tr, c1part)

		score = 0 
		for x, c2 in enumerate(cipherList):
			#print("cross element", x)
			lc2 = len(c2)

			c2part = c2[ii:ii+lt]

			if lc2 < ii+lt:
				continue
			if c1part == c2part:
				continue

			try:
				gp = fixed_xor(gk, c2part)
			except:
				continue

			score += trigramScore(gp)
			score += popularScore(gp)

		full_key.append([ii,ii+lt, score, gk])
	return full_key

def trigramScore(tr):
	if tr in trigrams:
		print('Found trigram')
		return 50
	return 0
def letterScore(binInput):
	score = 0
	base = string.ascii_uppercase
	for aa in binInput.upper():
		if aa in base:
			score += 1
	return score

def popularScore(binInput):
	score = 0
	base = b'ETAOIN SHRDLU'
	base = b' NIOATE'
	for aa in binInput.upper():
		sr = base.find(aa) + 1
		score += sr * 3
	return score

def isAllPrintable(binInput):
	res = True
	for ll in binInput:
		if chr(ll) not in string.printable:
			res = False
	return res


def test_challenge19():
	gkey = analysis()
	decryptAll(gkey)


		

if __name__ == "__main__":
	test_challenge19()







