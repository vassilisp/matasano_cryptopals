from c11 import randomPad, getRandom, repetitions
from c9 import pad, unpad
from c7 import encrypt as ecb_encrypt

from base64 import b64decode

from utils import assert_equals, asq

def encryption_oracle(bin_input):
	global key

	bin_input += appText
	padded = pad(bin_input, 16)
	return ecb_encrypt(key, padded)


def findBlockSize_old(oracle):
	res = 0
	for i in range(1,128):
		inp = i*b"A"
		enc = oracle(inp)
		reps = repetitions(enc)
		#print("input", inp, "repetitions", reps)
		if repetitions(enc) != 0:
			res = i/2
			break
	return res

def findBlockSize(oracle):
	t1 = len(oracle(b''))
	t2 = t1
	i = 0
	while t2 == t1:
		t2 = len(oracle(b'A'*i))
		i += 1
	return abs(t2 - t1)


def detectECB(oracle):
	enc = oracle(64*b"A")
	res = False
	if repetitions(enc) != 0:
		res = True
	return res


def find_next_char(oracle, block_size, known=b''):
	dic = {}
	tlen = block_size - (len(known)%block_size) - 1
	inp = bytes(tlen*b'A') 
	for i in range(256):
		t = inp + known + bytes([i])
		enc = oracle(t)
		dic[enc[:len(t)]] = i

	enc2 = oracle(bytes(inp))
	try:
		res = dic[enc2[:len(t)]]
	except:
		res = None
	return res

def findAll(oracle):
	res = b''
	while True:
		char = find_next_char(oracle, 16, res)
		if char == None:
			break
		print(char)
		res += bytes([char])


	res = unpad(res)
	return res

def test_challenge12():

	if not detectECB(encryption_oracle):
		return False
	block_size = findBlockSize(encryption_oracle)
	print("Block size:", block_size)
	res = findAll(encryption_oracle)
	print("RESULT", res)
	assert_equals(res, appText, 'Challenge 12 decryption')
	
	
key = getRandom(16)
appText = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")



if __name__ == "__main__":
	assert_equals = asq
	test_challenge12()



