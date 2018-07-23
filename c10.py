from utils import *
from c9 import pad, unpad
from c2 import fixed_xor3 as fixed_xor
from c7 import encrypt, decrypt
from c6 import read_b64_file

import binascii

def cbc_encrypt(iv, key, bin_input, blockSize=16):
#pad first
#split in blocks
#xor first block with iv and encrypt
#xor encrypted block with next bloc and encrypt
	bin_input = pad(bin_input, blockSize)
	res = bytearray()
	enc_block = iv
	for i in range(0, len(bin_input), blockSize):
		#print(i)
		block = bin_input[i : (i+blockSize)]
		xored_block = fixed_xor(block, enc_block)
		enc_block = encrypt(key, xored_block)
		res.extend(enc_block)
	return bytes(res)

def cbc_decrypt(iv, key, enc_input, blockSize=16):
#split in blocks
#decrypt and xor with iv
#decrypt and xor with previous cipher
	res = bytearray()
	pc_block = iv
	for i in range(0, len(enc_input), blockSize):
		#print(i)
		c_block = enc_input[i : (i+blockSize)]
		i_block = decrypt(key, c_block)

		p_block = fixed_xor(pc_block, i_block)
		pc_block = c_block

		res.extend(p_block)
	res = unpad(res)
	return res

#----------------------------------------
iv = bytes(16)
key = "YELLOW SUBMARINE"

def test_encr_decr_round():

	ciphert = cbc_encrypt(iv, key, text)
	#print("ciphertext:", ciphert)
	plaint = cbc_decrypt(iv, key, ciphert)
	#print("plaintext:", plaint)
	test(plaint, text, "encrypt/decrypt round test")

def test_encr_decr_round_rnd_iv():
	iv2 = bytearray(16)
	iv2[0] = 1
	ciphert = cbc_encrypt(iv2, key, text)
	#print("ciphertext:", ciphert)
	plaint = cbc_decrypt(iv2, key, ciphert)
	#print("plaintext:", plaint)
	test(plaint, text, "encrypt/decrypt round test - second IV")

def test_vectors():
	key=binascii.unhexlify('2b7e151628aed2a6abf7158809cf4f3c')
	iv=binascii.unhexlify('000102030405060708090A0B0C0D0E0F')
	plain=binascii.unhexlify('6bc1bee22e409f96e93d7e117393172a')
	cipher=binascii.unhexlify('7649abac8119b246cee98e9b12e9197d')
	calc_cipher = cbc_encrypt(iv, key, plain)
	assert_equals(calc_cipher[:-16], cipher, "test vectors")

def test_vectors_rfc_48():
	key = binascii.unhexlify('6c3ea0477630ce21a2ce334aa746c2cd')
	iv = binascii.unhexlify('c782dc4c098c66cbd9cd27d825682c81')
	plain = b"This is a 48-byte message (exactly 3 AES blocks)"
	cipher = binascii.unhexlify('d0a02b3836451753d493665d33f0e8862dea54cdb293abc7506939276772f8d5021c19216bad525c8579695d83ba2684')

	calc_cipher = cbc_encrypt(iv, key, plain)
	assert_equals(calc_cipher[:-16], cipher, "test vectors 48 byte (3block input) from rfc)")

def test_challenge10():
	res = cbc_decrypt(iv, key, bin_input)
	print(res.decode())
	print("challenge 10 passed")
#----------------------------------------

bin_input = read_b64_file('10.txt')
text = b"YELLOW submarineYELLOW submarineYELLOW sub"

if __name__ == "__main__":
	assert_equals = asq
	test_encr_decr_round()
	test_encr_decr_round_rnd_iv()
	test_vectors()
	test_vectors_rfc_48()
	test_challenge10()




