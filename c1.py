import binascii
import codecs
import base64
from nose.tools import assert_equals

"""
note: all results are byte-representation - use .decode('utf-8') to turn them into strings
"""
def hex_to_base64(hex_input):
	bin_rep = binascii.unhexlify(hex_input)
	return base64.b64encode(bin_rep)


hex_input= '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
expected = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def test_challenge1():
	res1 = hex_to_base64(hex_input)
	assert_equals(res1.decode(), expected)

if __name__ == "__main__":
	test_challenge1()
	print("challenge 1 passed")


