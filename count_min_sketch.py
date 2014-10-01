from numpy import zeros, int32, arange, array
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
		epsilon : error factor
		delta : the probability of error
		For the full paper on the algorithm, see the paper
		"An improved data stream summary: the count-min sketch and its -
		applications" by Cormode and Muthukrishnan, 2003.
		"""
		
		if epsilon is not None and delta is not None:
			w = int(ceil(e/epsilon))
			d = int(ceil(log(1./delta)))
		self.w = w
		self.d = d
		self.count = zeros((self.d, self.w), dtype=int32)
		self.rows = arange(self.d)
	
	def fnv64(self, a_string):
		in_bytes = bytearray(a_string)
		h = 0xcbf29ce484222325
		for byte in in_bytes:
			h *= 0x100000001b3
			h &= 0xffffffffffffffff
			h ^= byte
		return h
	
	def many_fnv64(self, a_string, n):
		hashes = zeros(n, dtype=int32)
		h = self.fnv64(a_string)
		w = self.w
		for i in xrange(n):
			cur = h%w
			h = (h - (cur)) / w
			hashes[i] = cur
			if i < n and h < w:
				h = self.fnv64(str(i) + a_string)
		return hashes
		
		
	def get_columns(self, a):
		w = self.w
		s = str(a)
		f = self.fnv64
		return self.many_fnv64(a, self.d)
		
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