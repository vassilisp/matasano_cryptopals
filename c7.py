from Crypto.Cipher import AES
from base64 import b64encode

import c6
from c9 import pad, unpad
#using openssl
#openssl enc -aes-128-ecb -d -K "59454C4C4F57205355424D4152494E45" -p -nosalt -in 7.txt -a

from utils import asq



def encrypt(key, text):
	cipher = AES.new(key, AES.MODE_ECB)
	res = cipher.encrypt(text)
	return res

def decrypt(key, enc):
	cipher = AES.new(key, AES.MODE_ECB)
	res = cipher.decrypt(enc)
	return res

def test_encr_decr_round():
	text = b"YELLOW submarine"
	key = b'YELLOW SUBMARINE'

	asq(decrypt(key, encrypt(key, text)), text, "encrypt/decrypt round test")

encrypted = c6.read_b64_file('7.txt')
key = b'YELLOW SUBMARINE'

if __name__ == "__main__":

	test_encr_decr_round()

	dec = decrypt(key, encrypted)
	res = dec.decode()
	print(res)

