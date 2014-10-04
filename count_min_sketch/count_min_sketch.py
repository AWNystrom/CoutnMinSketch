from numpy import zeros, int32, int16, arange, array
from math import log, e, ceil

class CountMinSketch(object):
	def __init__(self, w=None, d=None, delta=None, epsilon=None):#,
							#cache_size=0):
		"""
		CountMinSketch is an implementation of the count min sketch 
		algorithm that probabilistically counts string frequencies.
		
		Parameters
		----------
		w : the number of columns in the count matrix
		d : the number of rows in the count matrix

		For the full paper on the algorithm, see the paper
		"An improved data stream summary: the count-min sketch and its -
		applications" by Cormode and Muthukrishnan, 2003.
		"""
		
		self.w = w
		self.d = d
		self.count = zeros((self.d, self.w), dtype=int32)
		self.rows = arange(self.d)
		self.shift_by = int(ceil(log(w, 2)))
		
	def get_columns(self, a):
		a_string = str(a)
		d = self.d
		w = self.w
		shift_by = self.shift_by
		hashes = zeros(d, dtype=int16)
		
		prime = 0x1000000000000000000000000000000000000000163L
		offset = 0xdd268dbcaac550362d98c384c4e576ccc8b1536847b6bbb31023b4c8caee0535L
		mod = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffL
		
		#Hash
		in_bytes = bytearray(a_string)
		h = offset
		for byte in in_bytes:
			h *= prime
			h &= mod
			h ^= byte
		#/Hash
		
		times_hashed = 1
		for i in xrange(d):
			hashes[i] = h % w
			h >>= shift_by
			if h < w and i < d:
				#Hash
				times_hashed += 1
				in_bytes = bytearray(str(i) + a_string)
				h = offset
				for byte in in_bytes:
					h *= prime
					h &= mod
					h ^= byte
				#/Hash
				
		return hashes
		
	def update(self, a, val=1):
		#h, in_cache = self.cache.lookup(a)
		h = self.get_columns(a)
		self.count[self.rows, h] += val
	
	def query(self, a):
		#h, in_cache = self.cache.lookup(a)
		h = self.get_columns(a)
		return self.count[self.rows, h].min()
	
	def __getitem__(self, a):
		return self.query(a)
	
	def __setitem__(self, a, val):
		cur = self.query(a)
		self.update(a, val-cur)