import c3
import binascii

from nose.tools import assert_equals
from utils import asq

def test_challenge4():
	with open('4.txt') as f:
		out = []
		for i, line in enumerate(f):
			hex_input = line.replace('\n', '')
			#print(hex_input)
			bin_input = binascii.unhexlify(hex_input)
			try:
				res = c3.find_top(bin_input)
				print(i, res)
				out.append([i, res])
				#out format [line nr, [scr, xor_value, result]]
			except:
				#print(i, "no matches")
				pass
	
	out.sort(reverse=True, key=lambda kv: kv[1][0])
	print("RESULT")
	print(out[0])

	assert_equals(out[0][0], 170, "challenge 4")


if __name__ == "__main__":
	assert_equals = asq
	test_challenge4()
			
