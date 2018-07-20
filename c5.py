import binascii

def repeating_key_xor(original, key):
	"""original in binary, key in binary """
	if type(original) is not bytes:
		original = original.encode()
		print("original not in bytes, encoding")
	if type(key) is not bytes:
		key = key.encode()
		print("key not in bytes, encoding")

	#res = bytearray(len(original))
	#for i, byte in enumerate(original):
	#	res[i] = byte ^ key[i%len(key)] 
	#return res
	res = [byte ^ key[i%len(key)] for i, byte in enumerate(original)]
	return bytes(res)

if __name__ == "__main__":
	plaintext= """Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"""

	#plaintext= """Burning 'em, if you ain't quick and nimble\n"""
	#bin_plaintext = plaintext.encode()
	enc = repeating_key_xor(plaintext, b'ICE')
	#print(enc)
	res = binascii.hexlify(enc).decode()

	print(res)
	encodedExpectedY = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
	assert res == encodedExpectedY
	print("PASSED")

