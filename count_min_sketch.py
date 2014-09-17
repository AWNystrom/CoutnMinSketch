from numpy import zeros, int32, arange, array
from hashlib import md5

class CountMinSketch(object):
	def __init__(self, w, d, f=md5):
		"""
		w: the number of columns in the count matrix
		d: the number of rows in the count matrix
		f: the hash function class to be used. Must have the method hexdigest
		
		For the full paper on the algorithm, see the paper
		"An improved data stream summary: the count-min sketch and its -
		applications" by Cormode and Muthukrishnan, 2003.
		"""
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
		if val < 1:
			return
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