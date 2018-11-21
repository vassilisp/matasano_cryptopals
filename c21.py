#mersenne twister

from utils import *

class MTwister():
	w, n, m, r= 32, 624, 397, 31

	a = 0x9908B0DF

	u = 11
	d = 0xFFFFFFFF

	s = 7
	b = 0x9D2C5680

	t = 15
	c = 0xEFC60000

	l = 18
	f = 1812433253

	_lower_mask = (2 ** r) - 1
	_lower_mask2 = (1 << r) - 1  
	assert _lower_mask == _lower_mask2

#int array of length n
	def __init__(self, seed):
		self._MT = [0 for i in range(self.n)]
		self._index = self.n

		self._MT[0] = seed

		self._upper_mask = self.lowerNbits(~self._lower_mask)
		self._upper_mask2 = 2 ** self.r
		assert self._upper_mask == self._upper_mask2

		self._seed_mt(seed)

	def lowerNbits(self, inp):
		return (( 1 << self.w) - 1) & inp

	def _seed_mt(self, seed):
		for i in range(1, self.n):
			x =self.f * (self._MT[i-1] ^ self._MT[i-1] >> (self.w-2)) + i  
			self._MT[i] = self.lowerNbits(x)
		print("DONE SEEDING")


	def extract_number(self):
		if self._index >= self.n:
			self._twist()
		
		y = self._MT[self._index]
		y ^= ((y >> self.u) & self.d)
		y ^= ((y << self.s) & self.b)
		y ^= ((y << self.t) & self.c)
		y ^= ( y >> self.l)

		self._index += 1
		return self.lowerNbits(y)

	def _twist(self):
		for i in range(self.n):
			x0 = (self._MT[i] & self._upper_mask)
			x1 = (self._MT[(i+1) % self.n] & self._lower_mask)
			x = self.lowerNbits(x0 + x1)

			self._MT[i] = self._MT[(i + self.m) % self.n] ^ (x >> 1) 

			if (x % 2) != 0:
				self._MT[i] ^= self.a
		self._index = 0		

def mtwister_verification(vector_file):
	with open(vector_file) as f:
		vectors = f.read()
	vectors = vectors.split('\n\n')
	seed = vectors[0]
	seed = seed.replace('seed: ','')
	seed = int(seed)

	vectors = vectors[1].split('\n')
	vectors = vectors[:-1]

	#print(vectors)

	mt = MTwister(seed) 

	for i, vec in enumerate(vectors):
		rnd = mt.extract_number()
		assert_equals(rnd, int(vec), "Testing with output vector i: " + str(i) + ", val:" + str(rnd))

def test_mtwister_v1():
	mtwister_verification('21.txt')

def test_mtwister_v2():
	mtwister_verification('21b.txt')


if __name__ == "__main__":
	assert_equals = asq
	test_mtwister_v1()
	test_mtwister_v2()
