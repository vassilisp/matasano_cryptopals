from c6 import read_b64_file
from c18 import ctr_encrypt

from base64 import b64decode
from tools import getRandom, fixed_xor

def read_file(filename):
	res = []
	with open(filename) as f:
		for line in f:
			res.append(b64decode(line))
	return res


def getEncryptedList():
	res = []
	key = getRandom(16)
	plainList = read_file('20.txt')
	for entry in plainList:
		cipher = ctr_encrypt(key, entry)
		res.append(cipher)
	return res

def test_challenge20():

	cipherList = getEncryptedList()
	lList = [len(k) for k in cipherList]
	minim = min(lList)
	allciphers = b''
	for elem in cipherList:

		allciphers += elem[:minim]
	print(allciphers)

	from c6b import analyze
	key = analyze(allciphers, minim)
	print(key)

	res = []
	for cipher in cipherList:
		plain = fixed_xor(key, cipher[:minim])
		print(plain)





if __name__ == "__main__":
	test_challenge20()


