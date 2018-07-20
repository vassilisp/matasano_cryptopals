import binascii

from utils import asq, assert_equals

def fixed_xor(bin_input1, bin_input2):

	if len(bin_input1) == len(bin_input2):
		res = bytearray(len(bin_input1))
		for i in range(len(bin_input1)):
			res[i] = bin_input1[i] ^ bin_input2[i]
	return res



def fixed_xor2(bin_input1, bin_input2):

	if len(bin_input1) == len(bin_input2):
		res = bytearray(len(bin_input1))
		for i, (x,y) in enumerate(zip(bin_input1, bin_input2)):
			res[i] = x ^ y
	return res

def fixed_xor3(bin_input1, bin_input2):
	if len(bin_input1) == len(bin_input2):
		return bytes([x ^ y for x,y in zip(bin_input1, bin_input2)])

def test_challenge2_xor():
	res1 = fixed_xor(bin_input1, bin_input2)
	res1 = binascii.hexlify(res1).decode()
	assert_equals(res1, expected, 'xor1')

def test_challenge2_xor2():
	res2 = fixed_xor2(bin_input1, bin_input2)
	res2 = binascii.hexlify(res2).decode()
	assert_equals(res2, expected, 'xor2')

def test_challenge2_xor3():
	res3 = fixed_xor3(bin_input1, bin_input2)
	res3 = binascii.hexlify(res3).decode()
	assert_equals(res3, expected, 'xor3')


input1 = "1c0111001f010100061a024b53535009181c"
input2 = "686974207468652062756c6c277320657965"
expected = "746865206b696420646f6e277420706c6179"

bin_input1 = binascii.unhexlify(input1)
bin_input2 = binascii.unhexlify(input2)

if __name__ == "__main__":

	assert_equals = asq
	test_challenge2_xor()
	test_challenge2_xor2()
	test_challenge2_xor3()
	print("challenge 2 passed")





