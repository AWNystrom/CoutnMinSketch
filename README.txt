#CountMinSketch
==============

This is a pure-Python count-min sketch. It's pretty fast and accurate. Try it out!

##Usage
```python
>>> cms = CountMinSketch(200, 500)
>>> cms['foo']
0
>>> cms['foo'] += 5
>>> cms['foo']
5
```
