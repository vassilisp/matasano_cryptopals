from c11 import getRandom
from c9 import pad, unpad
from c10 import cbc_encrypt, cbc_decrypt
from c15 import checkPadding, PaddingException

from random import randint
from base64 import b64decode 
from utils import *

key = getRandom(16)

def encrypt():
	global key
	i = randint(0,9)
	item = inputList[i]
	item = b64decode(item)
	return cbcEncryptIv(key, item )

def decrypt(cipher):
	global key

	res = False
	try:
		cbcDecryptIv(key, cipher)
		res = True
	except PaddingException:
		print("XX - Padding Exception Caught")
		pass
	return res

def cbcEncryptIv(key, binInput):
	
	padded = pad(binInput, 16)
	iv = getRandom(16)
	cipher = cbc_encrypt(iv, key, padded)
	return iv + cipher


def cbcDecryptIv(key, cipherInput):

	iv = cipherInput[:16]
	cipher = cipherInput[16:]

	plain = cbc_decrypt(iv, key ,cipher)

	checkPadding(plain)
	return unpad(plain)

#----------------------------------------

key = "YELLOW SUBMARINE"
text = b"YELLOW submarineYELLOW submarineYELLOW sub"

def test_enc_dec_round():

	ciphert = cbcEncryptIv(key, text)
	print("ciphertext:", ciphert)
	plaint = cbcDecryptIv(key, ciphert)
	print("plaintext:", plaint)
	assert_equals(plaint, text, "encrypt/decrypt round test")

def test_double_enc_differ():

	cipher1 = cbcEncryptIv(key, text)
	cipher2 = cbcEncryptIv(key, text)
	asnq(cipher1, cipher2, "encrypt twice should differ")

def test_wrong_padding_dec():
	for i in range(256):
		tryWrongPadding(i)
	ass(True, "wrong padding test")

def tryWrongPadding(pad):
	enc = encrypt()
	res = decrypt(enc[:-1] + bytes([pad]))
	return res

def test_decrypt_wrong_padding():
	asq(tryWrongPadding(2), False, "wrong padding decryption expected result")
#----------------------------------------

INPUT="""MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"""
inputList = INPUT.split('\n')

if __name__ == "__main__":
	assert_equals = asq
	test_enc_dec_round()
	test_double_enc_differ()
	test_wrong_padding_dec()
	test_decrypt_wrong_padding()

