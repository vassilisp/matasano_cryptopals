import binascii
import c6

from utils import *

def test_challenge8():
	filename = '8.txt'
	with open(filename) as f:
		res = []
		for i, line in enumerate(f):
			line = line.replace("\n", "")

			bin_line = binascii.unhexlify(line)
			res.append([i, c6.hamming_keys(bin_line, 16, -1 )])

	res.sort(key=lambda kv: kv[1] )

	print("top 3")
	print(res[:3])
	out = res[0][0]
	print("result:", out )
	assert_equals(out, 132, "challenge 8 guess")

if __name__ == "__main__":
	assert_equals = asq
	test_challenge8()
