from utils import test
from c9 import pad, unpad
from c2 import fixed_xor3 as fixed_xor
from c7 import encrypt, decrypt
from c6 import read_b64_file

block_size = 16
def cbc_encrypt(iv, key, bin_input):
#pad first
#split in blocks
#xor first block with iv and encrypt
#xor encrypted block with next bloc and encrypt
	bin_input = pad(bin_input, block_size)
	res = bytearray()
	enc_block = iv
	for i in range(0, len(bin_input), block_size):
		#print(i)
		block = bin_input[i : (i+block_size)]
		xored_block = fixed_xor(block, enc_block)
		enc_block = encrypt(key, xored_block)
		res.extend(enc_block)
	return bytes(res)

def cbc_decrypt(iv, key, enc_input):
#split in blocks
#decrypt and xor with iv
#decrypt and xor with previous cipher
	res = bytearray()
	pc_block = iv
	for i in range(0, len(enc_input), block_size):
		#print(i)
		c_block = enc_input[i : (i+block_size)]
		i_block = decrypt(key, c_block)

		p_block = fixed_xor(pc_block, i_block)
		pc_block = c_block

		res.extend(p_block)
	res = unpad(res)
	return res

iv = bytes(block_size)
key = "YELLOW SUBMARINE"

def test1():
	text = b"YELLOW submarineYELLOW submarineYELLOW sub"

	ciphert = cbc_encrypt(iv, key, text)
	#print("ciphertext:", ciphert)
	plaint = cbc_decrypt(iv, key, ciphert)
	#print("plaintext:", plaint)
	test(plaint, text, "encrypt/decrypt round test")

	iv2 = bytearray(block_size)
	iv2[0] = 1
	ciphert = cbc_encrypt(iv2, key, text)
	#print("ciphertext:", ciphert)
	plaint = cbc_decrypt(iv2, key, ciphert)
	#print("plaintext:", plaint)
	test(plaint, text, "encrypt/decrypt round test - second IV")


if __name__ == "__main__":
	test1()

	bin_input = read_b64_file('10.txt')

	res = cbc_decrypt(iv, key, bin_input)
	print(res.decode())



