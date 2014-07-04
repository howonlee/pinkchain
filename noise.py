import numpy
import scipy
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
	#8.167% a's, 1.492% b's, etc
	prior = numpy.array([8167, 1492, 2782, 4253, 13000, 2228, 2015, 6094, 6966, 153, 772, 4025, 2406, 6749, 7507, 1929, 95, 5987, 6327, 9056, 2758, 978, 2360, 150, 1974, 74])
	dirichlet_draw = numpy.random.dirichlet(prior)
	#draw a multinomial from the dirichlet
	num_letters = 26
	#write it out in a matrix, everybody, to find the right axes for numpy calc
	letters_array = numpy.array(list(string.ascii_lowercase))
	values = [numpy.random.dirichlet(prior) for i in xrange(depth)]
	smooth = [numpy.random.dirichlet(prior) for i in xrange(depth)]
	source = [numpy.random.dirichlet(prior) for i in xrange(depth)]
	val_sum = sum(values) #across the right dimension
	i = 0
	while True:
		probs = abs(val_sum + smooth[i]) / sum(abs(val_sum + smooth[i]))
		yield numpy.random.choice(letters_array, p=probs)
		#yield a sample from the distribution, actually
		#there's a numpy thing for this
		i += 1
		if i == depth:
			i = 0
			#natural place to do a beyesian inference thingy
			smooth = [numpy.random.dirichlet(prior) for i in xrange(depth)]
			source = [numpy.random.dirichlet(prior) for i in xrange(depth)]
			continue
		c = 0
		while not (i >> c) & 1: #count trailing zeroes
			c += 1
		val_sum += source[i] - values[c] #take abs
		values[c] = source[i] #do right dimension

def markov_letter_iterpink_uniform(depth=20):
	num_letters = 26
	#write it out in a matrix, everybody, to find the right axes for numpy calc
	letters_array = numpy.array(list(string.ascii_lowercase))
	values = [numpy.random.randn(num_letters) for i in xrange(depth)]
	smooth = [numpy.random.randn(num_letters) for i in xrange(depth)]
	source = [numpy.random.randn(num_letters) for i in xrange(depth)]
	val_sum = sum(values) #across the right dimension
	i = 0
	while True:
		probs = abs(val_sum + smooth[i]) / sum(abs(val_sum + smooth[i]))
		yield numpy.random.choice(letters_array, p=probs)
		#yield a sample from the distribution, actually
		#there's a numpy thing for this
		i += 1
		if i == depth:
			i = 0
			smooth = [numpy.random.randn(num_letters) for i in xrange(depth)]
			source = [numpy.random.randn(num_letters) for i in xrange(depth)]
			continue
		c = 0
		while not (i >> c) & 1: #count trailing zeroes
			c += 1
		val_sum += source[i] - values[c] #take abs
		values[c] = source[i] #do right dimension

if __name__ == "__main__":
	pinknoise_to_file(float_iterpink)
	pinkletters_to_file(markov_letter_iterpink)
