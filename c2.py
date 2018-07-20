import binascii
from c9 import test

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

input1 = "1c0111001f010100061a024b53535009181c"
input2 = "686974207468652062756c6c277320657965"
expected = "746865206b696420646f6e277420706c6179"

bin_input1 = binascii.unhexlify(input1)
bin_input2 = binascii.unhexlify(input2)

if __name__ == "__main__":

	res1 = fixed_xor(bin_input1, bin_input2)
	res2 = fixed_xor2(bin_input1, bin_input2)

	res1 = binascii.hexlify(res1).decode()
	res2 = binascii.hexlify(res2).decode()

	res3 = fixed_xor3(bin_input1, bin_input2)
	res3 = binascii.hexlify(res3).decode()

	#print(res1)
	#print(res2)
	#print(res3)
	test(res1, expected)
	test(res2, expected)
	test(res3, expected)



