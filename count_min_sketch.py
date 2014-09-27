from numpy import zeros, int32, arange, array
from hashlib import md5
from math import log, e, ceil

import lru_cacher

def fnv64(a_string):
	in_bytes = bytearray(a_string)
	h = 0xcbf29ce484222325
	for byte in in_bytes:
		h *= 0x100000001b3
		h &= 0xffffffffffffffff
		h ^= byte
	return h

class CountMinSketch(object):
	def __init__(self, w=None, d=None, delta=None, epsilon=None, f=fnv64,
							cache_size=0):
		"""
		CountMinSketch is an implementation of the count min sketch 
		algorithm that probabilistically counts string frequencies.
		
		Parameters
		----------
		w : the number of columns in the count matrix
		d : the number of rows in the count matrix
		f : the hash function class to be used. Must be callable. By default
				the fnv64 hash function is used, which is very fast and good for
				w values less than 2^64.
		delta : the probability the error factor will hold.
		For the full paper on the algorithm, see the paper
		"An improved data stream summary: the count-min sketch and its -
		applications" by Cormode and Muthukrishnan, 2003.
		"""
		
		if epsilon is not None and delta is not None:
			w = ceil(e/epsilon)
			d = ceil(log(1./delta))
		self.w = w
		self.d = d
		self.f = f
		self.count = zeros((self.d, self.w), dtype=int32)
		self.rows = arange(self.d)
		self.cache_size = cache_size
		self.cache = lru_cacher.LruCacher(cache_size, self.get_columns)

	def get_columns(self, a):
		w = self.w
		s = str(a)
		f = self.f
		return array([f(str(i)+s) % w for i in xrange(self.d)])
		
	def update(self, a, val=1):
		h = self.get_columns(a)
		self.count[self.rows, h] += val
	
	def query(self, a):
		h, in_cache = self.cache.lookup(a)
		return self.count[self.rows, h].min()
	
	def __getitem__(self, a):
		return self.query(a)
	
	def __setitem__(self, a, val):
		cur = self.query(a)
		self.update(a, val-cur)