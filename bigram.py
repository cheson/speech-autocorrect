'''
This file takes in a corpus (in .txt) and outputs a dictionary of bigram costs. 
------------------
Data structure of output is as follows. Each entry is a {key: value} pair, 
where key = word1
and value = [ (word2, probability of word2 | word1), (word3, probability of word3 | word 1) ... ] 
'''
# import sys, string
import nltk, sys, string, collections, json
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter

# Class: BigramCost
# ---------------------
# Create and extract values from BigramCost dictionary
# class BigramCost(object):


# Function: create bigram (reads data into a dictionary)
# Output: [(word 1, word2), (word2, word3)...]
# >>> text = ["this is a sentence", "so is this one"]
# >>> bigrams = [b for l in text for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
# >>> print(bigrams)
# [('this', 'is'), ('is', 'a'), ('a', 'sentence'), ('so', 'is'), ('is', 'this'), ('this',     
# 'one')]
# ---------------------
# Note: this is the step before creating bigram costs -- creating a dictionary of 
inFile = sys.argv[1]
outFile = sys.argv[2]

bigramCost = collections.defaultdict(list)

with open(inFile, 'r') as i: 
	text = i.read()
	text = text.translate(None, string.punctuation)
	token = nltk.word_tokenize(text)
	bigrams = Counter(ngrams(token,2))
	
	# tally bigrams into bigramCost
	for pair in bigrams:
		# print pair
		entry = (pair[1], bigrams[pair])
		bigramCost[pair[0]].append(entry)
		 
	# normalize bigramCost based on the total number of words in the first word 
	# to get (word2, probability of word2 | word1)
	# TODO: To write, but not sure if it is worthwhile writing it as we still don't know what form to put

	print bigramCost

with open(outFile, 'w') as fp: 
	json.dump(bigramCost, fp)



# def createBigram(data): 
# 	bigrams = [b for l in text for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
# 	print(bigrams)
# 	return bigrams 

# test this with sample.txt before going to write the next step