from c9 import pad, unpad
from c10 import cbc_encrypt, cbc_decrypt
from c11 import getRandom
from c12 import findBlockSize

from random import randint
from utils import *

prep = b"comment1=cooking%20MCs;userdata="
app = b";comment2=%20like%20a%20pound%20of%20bacon"
lprep = len(prep)

key = None
def encrypt(binInput):
	global key
	if key == None:
		key = getRandom(16)

	binInput = binInput.replace(b';', b'').replace(b'=',b'')
	inp = prep + binInput + app

	inp = pad(inp, 16)
	iv = getRandom(16)
	return iv + cbc_encrypt(iv, key, inp)


def decrypt(binInput):
	global key

	enc = binInput[16:]
	iv = binInput[:16]
	padded = cbc_decrypt(iv, key, enc)
	plain = unpad(padded)
	#print(plain)
	return plain

def check(binInput):
	out = decrypt(binInput)
	res = False
	if b';admin=true;' in out:
		print("CIPHER --  ", binInput)
		print("PLAIN  --  ", out)
		res = True
	return res

#----------------------------------------
def test_enc_dec_round():
	inp = b'YELLOW SUBMARINE'
	enc = encrypt(inp)
	asn(check(enc), 'encryption/decryption round')

def test_not_allowed_signs():
	inp = b'admin=true'
	enc = encrypt(inp)
	res = check(enc)
	asn(res, 'not allowed sign check')

def test_not_allowed_signs_period():
	inp = b'admin=true;true;'
	enc = encrypt(inp)
	out = decrypt(enc)

	asn(b'true;true' in out, 'not allowed sign check - ;')

#----------------------------------------
def inputForNewBlock(blockSize, prepSize):
	inLen = blockSize - (prepSize % blockSize)
	return inLen*b'A'
	
def injectCipherText(oracle, binInput, prepSize=None):
	if prepSize == None:
		prepSize = randint(0,len(oracle(b'')))

	bS = findBlockSize(oracle)

	in1 = inputForNewBlock(bS, prepSize)
	#print('block size:', bS)

	fillerBlock = bytes(bS)
	endBlock = binInput
	orgBlock = bytes(len(endBlock))
	if len(endBlock) > bS:
		raise Exception

	inp = in1 + fillerBlock + orgBlock
	enc = oracle(inp)

	start = prepSize + len(in1) + bS
	controlBlock = bytearray(enc)
	for i, char in enumerate(endBlock):
		loc = start + i 

		controlBlock[loc] ^= char

	return bytes(controlBlock)

def test_challenge16():
	print("CHALLENGE 16")
	modded = injectCipherText(encrypt, b';admin=true', lprep)
	res = check(modded)
	
	ass(res, 'challenge 16 test')

def test_challenge16_unknown_prep():
	print("CHALLENGE 16 === HARD")
	maxTries = 1000000
	res = False
	for i in range(maxTries):
		try:
#			modded = injectCipherTextUnknownPrep(encrypt, b';admin=true')
			modded = injectCipherText(encrypt, b';admin=true')
			res = check(modded)
		except:
			continue

		if i%100 == 0:
			print("TRY:", i)
		if res:
			print("FOUND IT IN TRY:", i)
			break

	
	ass(res, 'challenge 16 test - HARD')

if __name__ == "__main__":
	test_enc_dec_round()
	test_not_allowed_signs()
	test_not_allowed_signs_period()
	test_challenge16()
	test_challenge16_unknown_prep()
