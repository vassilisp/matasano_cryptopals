from utils import *

class PaddingException(Exception):
	"""Wrong padding exception"""
	pass

def checkPadding(binInput):
	paddingIndication = binInput[-1]
	for i in range(1, paddingIndication + 1):
		if binInput[-i] != paddingIndication:
			raise PaddingException


#========================================
def test_correct_pad():
	checkPadding(validPad)
	ass(True, 'correct pad')


def test_wrong_pad():
	try:
		checkPadding(wrongPad1)
	except PaddingException:
		ass(True, "wrong pad 1")


def test_wrong_pad2():
	try:
		checkPadding(wrongPad1)
	except PaddingException:
		ass(True, "wrong pad 1")

def test_completely_wrong_pad():
	try:
		checkPadding(completelyWrongPad)
	except PaddingException:
		ass(True, "completely wrong pad")

def test_challenge15():
	test_correct_pad()
	test_wrong_pad()
	test_wrong_pad2()

validPad = b"ICE ICE BABY\x04\x04\x04\x04"
wrongPad1 = b"ICE ICE BABY\x05\x05\x05\x05"
wrongPad2 = b"ICE ICE BABY\x01\x02\x03\x04" 
completelyWrongPad = b"ICE ICE BABY\x01\x02\x03=" 
#========================================

if __name__ == "__main__":
	assert_equals = asq
	test_correct_pad()
	test_wrong_pad()
	test_wrong_pad2()
	test_completely_wrong_pad()
	test_challenge15()




