from utils import *

def pad(bin_input, block_size):
	org_size = len(bin_input)
	padLen = block_size - (org_size % block_size)
	return bin_input.ljust(org_size + padLen, bytes([padLen]))


def unpad(bin_input):
	return bin_input[:-bin_input[-1]]


def test_pad_unpad_round():
	text = b"YELLOW submarine"
	test(unpad(pad(text, 16)), text, "pad/unpad round")

def test_pad_unpad_20():
	text = b"YELLOW submarine"
	test(unpad(pad(text, 20)), text, "pad/unpad round - size 20")

def test_challenge9():
	res = pad(bin_input, 20)
	assert_equals(res, expected, "c9 challenge")

bin_input = b'YELLOW SUBMARINE'
expected = b"YELLOW SUBMARINE\x04\x04\x04\x04" 

if __name__ == "__main__":

	assert_equals = asq
	test_pad_unpad_round()
	test_pad_unpad_20()
	test_challenge9()
