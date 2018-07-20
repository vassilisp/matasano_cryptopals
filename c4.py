

import c3
import binascii

if __name__ == "__main__":
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
			
