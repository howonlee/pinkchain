import numpy
import math
import random
import string
from itertools import *

def white(N):
	return numpy.random.randn(N)

def violet(N):
	return numpy.diff(numpy.random.randn(N))

def brown(N):
	return numpy.cumsum(numpy.random.randn(N))

#one-dimensional only
def pink(N, iterpink, depth=80):
	return list(islice(iterpink(depth), N))

def float_iterpink(depth=20):
	values = numpy.random.randn(depth)
	smooth = numpy.random.randn(depth)
	source = numpy.random.randn(depth)
	sum = values.sum()
	i = 0
	while True:
		yield sum + smooth[i]
		i += 1
		if i == depth:
			i = 0
			smooth = numpy.random.randn(depth)
			source = numpy.random.randn(depth)
			continue
		c = 0
		while not (i >> c) & 1: #count trailing zeroes
			c += 1
		sum += source[i] - values[c]
		values[c] = source[i]

def pinknoise_to_file(iterpink, N=10000):
	print "beginning..."
	n = pink(N, iterpink, depth=80)
	print "generated..."
	f0 = 10e6 #imagined carrier
	n = [x+f0 for x in n] #add noise and carrier
	fr = [(x-f0)/float(f0) for x in n] #fractional frequency
	print "starting the write..."
	with open('pinknoise_frequency.txt', 'w') as f:
		for ff in fr:
			f.write("%0.6g\n" % ff)
	print sum(n) / float(len(n))

def pinkletters_to_file(iterpink, N=10000):
	print "beginning..."
	n = pink(N, iterpink, depth=80)
	print "generated, starting the write..."
	with open('pinknoise_markov_letters.txt', 'w') as f:
		for ff in n:
			f.write("%s" % ff[-1])

def markov_letter_iterpink(depth=20):
	"""
	all of these are random choices from the alphabet instead of something else
	only use the dataset afterwards, to sample randomly from
	the dataset distribution instead of something else

	Args:
		dataset: The dataset to the 1st-order markov chain as,, as a dictionary
	Kwargs:
		depth: The depth of the signal filter
	"""
	#maybe I do want distributions, this doesn't not make sense
	values = [random.choice(string.ascii_lowercase) for n in xrange(depth)]
	smooth = [random.choice(string.ascii_lowercase) for n in xrange(depth)]
	source = [random.choice(string.ascii_lowercase) for n in xrange(depth)]
	#basically, I have to find an analogue to addition for strings
	#concatenations? sure, try it, see how it fucks up, it's temporary and specific
	#this is a weird hybrid of concatenations and other stuff
	sum = "".join(values)
	i = 0
	while True:
		yield sum + smooth[i]
		i += 1
		if i == depth:
			i = 0
			smooth = [random.choice(string.ascii_lowercase) for n in xrange(depth)]
			source = [random.choice(string.ascii_lowercase) for n in xrange(depth)]
			continue
		c = 0
		while not (i >> c) & 1: #count trailing zeroes
			c += 1
		sum += chr(abs(ord(source[i]) - ord(values[c]))) ##minus?
		values[c] = source[i]

def markov_word_iterpink(depth=20):
	"""
	Args:
		dataset: The dataset to the 1st-order markov chain as,, as a dictionary
	Kwargs:
		depth: The depth of the signal filter
	"""
	values = numpy.random.randn(depth)
	smooth = numpy.random.randn(depth)
	source = numpy.random.randn(depth)
	sum = values.sum()
	i = 0
	while True:
		yield sum + smooth[i]
		i += 1
		if i == depth:
			i = 0
			smooth = numpy.random.randn(depth)
			source = numpy.random.randn(depth)
			continue
		c = 0
		while not (i >> c) & 1: #count trailing zeroes
			c += 1
		sum += source[i] - values[c]
		values[c] = source[i]

if __name__ == "__main__":
	pinknoise_to_file(float_iterpink)
	pinkletters_to_file(markov_letter_iterpink)
