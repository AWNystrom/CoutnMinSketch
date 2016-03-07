from array import array
from random import randint
from math import log, e, ceil
from itertools import izip

class CountMinSketch(object):
	def __init__(self, w=None, d=None, delta=None, epsilon=None, bits=256):
		"""
		CountMinSketch is an implementation of the count min sketch 
		algorithm that probabilistically counts string frequencies.
		
		You must either supply w and d directly, or let them be calculated form error,
		delta, and epsilon. If You choose the latter, then w = ceil(error/epsilon) and
		d = ceil(ln(1.0/delta)) where the error in answering a query is within a factor 
		of epsilon with probability delta.
		
		Parameters
		----------
		w : the number of columns in the count matrix
		d : the number of rows in the count matrix
		delta : (not applicable if w and d are supplied) the probability of query error
		epsilon : (not applicable if w and d are supplied) the query error factor

		bits : The size of the hash output space
		
		For the full paper on the algorithm, see the paper
		"An improved data stream summary: the count-min sketch and its -
		applications" by Cormode and Muthukrishnan, 2003.
		"""
		
		if w is not None and d is not None:
			self.w = w
			self.d = d
		elif delta is not None and epsilon is not None:
			self.w = int(ceil(e/epsilon))
			self.d = int(ceil(log(1./delta)))
			print self.w, self.d
		else:
			raise Exception("You must either supply both w and d or delta and epsilon.")
		
		if 2**bits < w:
			raise Exception("Too few bits for w")
		
		self.counts = [array('L', (0 for _ in xrange(self.w))) for _ in xrange(self.d)]
		self.mask = array('L', (randint(0, 2147483647) for _ in xrange(self.d-1)))
		
	def get_columns(self, a):
		h = hash(a)
		w = self.w
		
		yield h % w
		for m in self.mask:
			h ^= m
			yield h % w
	
	def old_get_columns(self, a):
		h = hash(a)
		w = self.w
		
		#yield h % w
		for i in xrange(self.d):
			#h ^= m
			#yield h % w
			yield hash((i, h)) % w
	
	def old_get_columns(self, a):
		h = hash(a)#xxh32(a).intdigest()
		original_h = int(h)
		w = self.w
		shift_by = self.shift_by
		
		for m in self.mask:
			yield h % w
			h >>= shift_by
			if h < w:# and i < d:
			  h  = original_h ^ m
		
	def update(self, a, val=1):
		#h, in_cache = self.cache.lookup(a)
		for row, col in izip(self.counts, self.get_columns(a)):
		  row[col] += val
	
	def query(self, a):
		return min(row[col] for row, col in izip(self.counts, self.get_columns(a)))
	
	def __getitem__(self, a):
		return self.query(a)
	
	def __setitem__(self, a, val):
		self.update(a, val)