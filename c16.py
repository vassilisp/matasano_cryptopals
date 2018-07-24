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
	print(plain)
	return plain

def check(binInput):
	out = decrypt(binInput)
	res = False
	if b';admin=true;' in out:
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

def inputForNewBlock(blockSize):
	inLen = blockSize - (lprep % blockSize)
	return inLen*b'A'
	

def test_challenge16():
	bS = findBlockSize(encrypt)

	in1 = inputForNewBlock(bS)
	in1 = b''
	print(bS)
	print(lprep)

	controlBlock = bytearray(16)
	modBlock = b'XadminXtrue'
	loc1 = 0
	loc2 = 6

	inp = in1 + bytes(controlBlock) + modBlock
	enc = encrypt(inp)

	start = lprep + len(in1) + bS

	loc1 = loc1 + start 
	loc2 = loc2 + start

	modBlock = bytearray(enc)
	modBlock[loc1] = ord('X') ^ ord(';') ^ enc[loc1]
	modBlock[loc2] = ord('X') ^ ord('=') ^ enc[loc2]
	mod_enc = bytes(modBlock)
	res = check(mod_enc)
	
	ass(res, 'challenge 16 test')

if __name__ == "__main__":
	test_enc_dec_round()
	test_not_allowed_signs()
	test_not_allowed_signs_period()
	test_challenge16()
