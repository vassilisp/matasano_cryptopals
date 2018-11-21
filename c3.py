import binascii
from utils import asq, assert_equals

def single_byte_xor(bin_input, xor_byte):
	""" input in bytes, xor_byte in int (0-127) """
	if type(bin_input) is not bytes:
		bin_input = bin_input.encode()

	res = bytearray(len(bin_input))
	for i, byte in enumerate(bin_input):
		res[i] = byte ^ xor_byte
	return res


def __freq_analysis(str_input):
	""" input should be string """
	dic = {}
	str_input_upper = str_input.upper()
	for i in str_input_upper:
		try:
			dic[i] += 1
		except:
			dic[i] = 1
	sorted_dic = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)
	return sorted_dic

#def __match_score(str_input, samples=10):
#	fanal = __freq_analysis(str_input)
#	baseline = "ETAOIN "
#	score = 0
#	if len(fanal) < samples:
#		samples = len(fanal)
#	for i in range(samples):
#		if fanal[i][0] in baseline:
#			score += 1
#	return score

def __match_score2(str_input):
	baseline = "ETAOIN "
	score = 0
	for i in str_input.upper():
		if i in baseline:
			score += 1
	return score

def find_topN(bin_input, N=1):
	""" enc input in bytes"""
	possible = []
	for i in range(256):
		res = single_byte_xor(bin_input, i)
		res_str = ""
		try:
			res_str = res.decode()
		except:
			#print("decoding error", i)
			continue

		possible.append([__match_score2(res_str), i])
	possible.sort(reverse=True)

	out = []
	for i in range(N):
		xor_value = possible[i][1]
		scr = possible[i][0]
		out.append([i, scr, xor_value, single_byte_xor(bin_input, xor_value).decode()])
	return out

def find_top(bin_input):
	res = find_topN(bin_input)
	return res[0][1:]

def test_challenge3():
	possible = find_top(bin_input)
	print(possible)
	assert_equals(possible[1], 88, "challenge 3")

hex_input = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
bin_input = binascii.unhexlify(hex_input)

if __name__ == "__main__":
	assert_equals = asq
	test_challenge3()

	
