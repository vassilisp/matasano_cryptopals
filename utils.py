from nose.tools import assert_equals

def ass(expression, name=""):
	if expression:
		print("PASSED -", name)
	else:
		print("FAILED -", name, " - input:", expression)
		raise Exception("expression match failed")

def asn(expression, name=""):
	ass(not expression, name)

def asq(org, expected, name=""):
	try:
		assert org == expected
		print("PASSED -", name)
	except AssertionError as ex:
		print("FAILED -", name, " - input:", org, " - expecte:", expected)

def asnq(org, expected, name=""):
	try:
		assert org != expected
		print("PASSED -", name)
	except AssertionError as ex:
		print("FAILED -", name, " - input:", org, " - expecte:", expected)

test = asq
