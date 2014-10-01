import countminsketch
import count_min_sketch
from time import time

mytime = 0
theirtime = 0

mine = count_min_sketch.CountMinSketch(1000, 5000)
theirs = countminsketch.CountMinSketch(1000, 5000)

for i in xrange(10000):
	t = time()
	mine.update('a')
	mytime += time() - t
	
	t = time()
	theirs.add('a')
	theirtime += time() - t
	
print mine['a'], theirs['a']
print mytime, theirtime