from utils import ass
from c7 import encrypt as ecb_encrypt, decrypt as ecb_decrypt
from c9 import pad, unpad
from c11 import getRandom
from c12 import findBlockSize, detectECB

def profile_parser(enc_profile):
	dic = {}
	for part in enc_profile.split("&"):
		kv = part.split('=')
		k = kv[0]
		try:
			v = kv[1]
		except:
			v = ''
		dic[k] = v
	return dic


def profile_for(email):
	if type(email) is not bytes:
		try:
			email = email.encode()
		except:
			email = bytes(email)

	email = email.replace(b"=", b"").replace(b"&", b"")
	return b"email=" + email + b"&uid=10&role=user" 


def getProfile(email):
	global key

	profile = profile_for(email)
	if type(profile) is not bytes:
		try:
			profile = profile.encode()
		except:
			profile = bytes(profile)

	padded = pad(profile, 16)
	return ecb_encrypt(key, padded)


def checkProfile(prof):
	global key

	plain = unpad(ecb_decrypt(key, prof))
	return plain



##========================================
##Failed attempts
#
#def fail_challenge13():
#
#	enc_admin = encrypt_as_last(b'admin')
#	enc_user = encrypt_as_last(b'user')
#
#	res = b''
#	for i in range(32):
#		encrypted = getProfile(i*b'A')
#		if enc_user in encrypted:
#			mod_encrypted = encrypted.replace(enc_user, enc_admin)
#			res = checkProfile(mod_encrypted)
#			print("DONE")
#			break
#
#	print(res)
#	if b'admin' in res:
#		print("WE DID IT")
#	
#def encrypt_as_last(bin_input):
#	block_size = 16
#
#	marker1 = b'email='
#	target = bin_input
#
#	lm1 = len(marker1)
#	lt = len(target)
##'email=vpan&uid=10&role=user'
#
##sanity checks
#	if lm1+lt>block_size:
#		print("target too big max len=", block_size-lm1)
#		return None
#
##use user provided input to encrypt admin as the last part of a block
#	fillerLen = (block_size -lm1 - lt)
#	start = lm1+fillerLen
#	stop = start+lt
#	user_input = marker1 + fillerLen*b'A' + target
#	enc_target = getProfile(user_input)[start:stop]
#	print(enc_target)
#	return enc_target
#
##========================================

def test_challenge13():
	block_size = 16
	marker = b'email='
	lm = len(marker)

	userInput1 = (block_size-lm)*b'A'
	userInput2 = pad(b'admin', 16)

	userInput3 = pad(b'user', 16)

	enc_admin_block = getProfile(userInput1 + userInput2)[16:32]
	test1 = profile_for(userInput1 + userInput2)
	finder = getProfile(userInput1 + userInput3)[16:32]
	
	res = b''
	for i in range(16):
		inp = i*b'A'
		test = profile_for(inp)
		encrypted = getProfile(inp)
		if finder in encrypted:
			mod_enc = encrypted[:-16] + enc_admin_block
			res = checkProfile(mod_enc)
			print("DONE")
			break

	print(res)
	ass(b'role=admin' in res, 'Challenge 13')
	


#========================================
def test_profile_parser():
	res = profile_parser("foo=bar&baz=qux&zap=zazzle")
	print(res)

def test_profile_for():
	res = profile_for('user@domain.com')
	print(res)

def test_profile_for_forbidden():
	res = profile_for('user@domain.com&role=admin')
	print(res)
	ass(b'role=admin' not in res, 'forbidden chars')

def test_get_check_profile():
	prof = 'user@domain.com'
	res = getProfile(prof)
	decoded = checkProfile(res)
	print(decoded)
	ass(prof.encode() in decoded, 'email check')
	ass(b'role=user' in decoded, 'role check')


key = getRandom(16)

if __name__ == "__main__":

	test_profile_parser()
	test_profile_for()
	test_profile_for_forbidden()
	test_get_check_profile()

	test_challenge13()


