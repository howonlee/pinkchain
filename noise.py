import numpy
import scipy
import math
import random
import string
import collections
import operator
import iterpinks
from itertools import *

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

def pinkwords_to_file(iterpink, N=200):
	#try first-order markov chain first, and then 3rd-order
	#the third-order one may take a while
	print "beginning parsing of corpus..."
	ct = collections.Counter()
	with open("total_corpus.txt", "r") as corpus:
		for line in corpus:
			line_processed = line.lower().translate(string.maketrans("",""), string.punctuation).split()
			for word in line_processed:
				ct[word] += 1
	markov_list = ct.items()
	markov_array = map(operator.itemgetter(1), markov_list)
	normalizer = math.log(sum(markov_array))
	markov_array = numpy.array(map(lambda x: math.exp(math.log(x) - normalizer), markov_array))
	word_array = map(operator.itemgetter(0), markov_list)
	print markov_array
	print "finished corpus fuckery. beginning generation..."
	n = list(islice(iterpink(markov_array, word_array), N))
	print "generated, starting the write..."
	with open('pinknoise_markov_words.txt', 'w') as f:
		f.write(" ".join(n))

def pink_semimarkov_letters_to_file(iterpink, ngram_order=3, N=500):
	#do third-order markov chain for all this shit
	print "beginning parsing of corpus..."
	ct = collections.Counter()
	with open("total_corpus.txt", "r") as corpus:
		for line in corpus:
			line_processed = list(line.lower().translate(string.maketrans("",""), string.punctuation))
			for ngram in zip(*[line_processed[i:] for i in range(ngram_order)]):
				ct["".join(ngram)] += 1
			#now the markov process
	markov_list = ct.items()
	markov_array = map(operator.itemgetter(1), markov_list)
	normalizer = math.log(sum(markov_array))
	print "length of markov list: ", len(markov_list)
	markov_array = numpy.array(map(lambda x: math.exp(math.log(x) - normalizer), markov_array))
	word_array = map(operator.itemgetter(0), markov_list)
	print markov_array
	print "finished corpus fuckery. beginning generation..."
	n = list(islice(iterpink(markov_array, word_array), N))
	print "generated, starting the write..."
	with open('pinknoise_semimarkov_words.txt', 'w') as f:
		f.write("".join(n))

def pink_semimarkov_words_to_file(iterpink, ngram_order=2, N=100):
	#do third-order markov chain for all this shit
	print "beginning parsing of corpus..."
	ct = collections.Counter()
	with open("total_corpus.txt", "r") as corpus:
		for line in corpus:
			line_processed = line.lower().translate(string.maketrans("",""), string.punctuation).split()
			for ngram in zip(*[line_processed[i:] for i in range(ngram_order)]):
				ct[" ".join(ngram)] += 1
			#now the markov process
	markov_list = ct.items()
	markov_array = map(operator.itemgetter(1), markov_list)
	normalizer = math.log(sum(markov_array))
	print "length of markov list: ", len(markov_list)
	markov_array = numpy.array(map(lambda x: math.exp(math.log(x) - normalizer), markov_array))
	word_array = map(operator.itemgetter(0), markov_list)
	print markov_array
	print "finished corpus fuckery. beginning generation..."
	n = list(islice(iterpink(markov_array, word_array), N))
	print "generated, starting the write..."
	with open('pinknoise_semimarkov_words.txt', 'w') as f:
		f.write(" ".join(n))

if __name__ == "__main__":
	#pinknoise_to_file(iterpinks.float_iterpink)
	#pinkletters_to_file(iterpinks.markov_letter_iterpink)
	#pinkwords_to_file(iterpinks.markov_word_iterpink)
	pink_semimarkov_words_to_file(iterpinks.markov_word_iterpink)
