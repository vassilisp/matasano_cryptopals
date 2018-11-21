from c7 import encrypt, decrypt

from tools import getBlocks, fixed_xor
from utils import *

from base64 import b64decode
import struct
from ctypes import c_uint32

def ctr_encrypt(key,  binInput, nonce=0, bS=16):

	blocks = getBlocks(binInput, bS)
	res = b''
	for block in blocks:
		#ctr = nonce.to_bytes(bS, byteorder='little', signed=False)
		ctr = toBytes(nonce)
		stream = encrypt(key, ctr)
		if len(block) < bS:
			stream = stream[:len(block)]
		enc = fixed_xor(stream, block)
		res += enc
		nonce += 1
	return res

def ctr_decrypt(key, binInput, nonce=0, bS=16):
	return ctr_encrypt(key, binInput, nonce, bS)

def toBytes(inInt):
	a = c_uint32(inInt)
	b = c_uint32(inInt >> 32)
	return struct.pack('<QQ', b.value, a.value)



#----------------------------------------
key = b"YELLOW SUBMARINE"

vector = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
vector = b64decode(vector)
dec_vector = b"Yo, VIP Let's kick it Ice, Ice, baby Ice, Ice, baby "

text = b'Decrypt the string at the top of this function, then use your CTR function to encrypt '

def test_ctr_round():
	enc = ctr_encrypt(key, text)
	print(enc)
	dec = ctr_decrypt(key, enc)
	assert_equals(dec, text, "ctr round")

def test_ctr_nonce():
	enc1 = ctr_encrypt(key, text)
	print(enc1)
	enc2 = ctr_decrypt(key, text, 1)
	print(enc2)
	asnq(enc1, enc2, "ctr different nonces")
	
def test_challenge_18():
	dec = ctr_decrypt(key, vector, 0)
	print(dec)
	assert_equals(dec, dec_vector, "challenge 18 decryption")


if __name__ == "__main__":
	assert_equals = asq
	test_ctr_round()
	test_ctr_nonce()
	test_challenge_18()
