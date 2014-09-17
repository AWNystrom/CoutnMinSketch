from numpy import zeros, int32, arange, array
from hashlib import md5
from math import log, e, ceil

class CountMinSketch(object):
	def __init__(self, w=None, d=None, delta=None, epsilon=None, f=md5):
		"""
		CountMinSketch is an implementation of the count min sketch 
		algorithm that probabilistically counts string frequencies.
		
		Parameters
		----------
		w : the number of columns in the count matrix
		d : the number of rows in the count matrix
		f : the hash function class to be used. Must have the method hexdigest
		epsilon : the error bound.
		delta : the probability the error bound will hold.
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

	def get_columns(self, a):
		w = self.w
		s = str(a)
		f = self.f
		return array([int(f(s+str(i)).hexdigest(), 16) % w for i in xrange(self.d)])
		
	def update(self, a, val=1):
		h = self.get_columns(a)
		self.count[self.rows, h] += val
	
	def query(self, a):
		h = self.get_columns(a)
		return self.count[self.rows, h].min()
	
	def __getitem__(self, a):
		return self.query(a)
	
	def __setitem__(self, a, val):
		cur = self.query(a)
		self.update(a, val-cur)