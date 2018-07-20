from utils import test
def pad(bin_input, block_size):
	org_size = len(bin_input)
	padLen = block_size - (org_size % block_size)
	return bin_input.ljust(org_size + padLen, bytes([padLen]))


def unpad(bin_input):
	return bin_input[:-bin_input[-1]]


bin_input = b'YELLOW SUBMARINE'
expected = b"YELLOW SUBMARINE\x04\x04\x04\x04" 

def test1():
	text = b"YELLOW submarine"
	test(unpad(pad(text, 16)), text, "pad/unpad round")

def test2():
	text = b"YELLOW submarine"
	test(unpad(pad(text, 20)), text, "pad/unpad round - size 20")

if __name__ == "__main__":
	res = pad(bin_input, 20)

	test1()
	test2()
	test(res, expected, "c9 challenge")
