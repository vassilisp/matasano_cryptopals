from utils import ass

class PaddingException(Exception):
	"""Wrong padding exception"""
	pass

def checkPadding(binInput):
	paddingIndication = binInput[-1]
	for i in range(1, paddingIndication + 1):
		if binInput[-i] != paddingIndication:
			raise PaddingException


def test_correct_pad():
	checkPadding(validPad)
	ass(True, 'correct pad')


def test_wrong_pad():
	try:
		checkPadding(wrongPad1)
	except:
		ass(True, "wrong pad 1")


def test_wrong_pad2():
	try:
		checkPadding(wrongPad1)
	except:
		ass(True, "wrong pad 1")

def test_challenge15():
	test_correct_pad()
	test_wrong_pad()
	test_wrong_pad2()

validPad = b"ICE ICE BABY\x04\x04\x04\x04"
wrongPad1 = b"ICE ICE BABY\x05\x05\x05\x05"
wrongPad2 = b"ICE ICE BABY\x01\x02\x03\x04" 

if __name__ == "__main__":
	test_challenge15()



