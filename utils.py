
def test(org, expected, name=""):
	try:
		assert org == expected
		print("PASSED -", name)
	except AssertionError as ex:
		print("FAILED -", name, " - input:", org, " - expecte:", expected)

def ntest(org, expected, name=""):
	try:
		assert org != expected
		print("PASSED -", name)
	except AssertionError as ex:
		print("FAILED -", name, " - input:", org, " - expecte:", expected)
