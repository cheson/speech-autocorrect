'''
This file takes in a corpus (in .txt) and outputs a dictionary of bigram costs. 
------------------
Data structure of output is as follows. Each entry is a {key: value} pair, 
where key = word1
and value = [ (word2, probability of word2 | word1), (word3, probability of word3 | word 1) ... ] 
'''
# import sys, string
import nltk, sys, string, collections, json, os 
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
# inFile = sys.argv[1]
path = sys.argv[1]
# inFile2 = "patientsmonologues.txt"
outFile = sys.argv[2]

bigramCost = collections.defaultdict(list)

for subdir, dirs, files in os.walk(path):
	for filename in files:
		filePath = subdir + '/' + filename
		with open(filePath, 'r') as i: 
			text = i.read()
			text = text.translate(None, string.punctuation)
			text = text.translate(None, string.digits)

			
			# print text
			# text = unicode(text, errors='ignore').encode("utf-8")
			token = nltk.word_tokenize(text)

			bigrams = Counter(ngrams(token,2))
			
			# tally bigrams into bigramCost
			for pair in bigrams:
				# print pair
				entry = (pair[1], bigrams[pair])
				bigramCost[pair[0]].append(entry)



# with open(inFile2, 'r') as i: 
# 	text = i.read()
# 	text = text.translate(None, string.punctuation)
# 	token = nltk.word_tokenize(text)
# 	bigrams = Counter(ngrams(token,2))
	
# 	# tally bigrams into bigramCost
# 	for pair in bigrams:
# 		# print pair
# 		entry = (pair[1], bigrams[pair])
# 		bigramCost[pair[0]].append(entry)
		 
	# normalize bigramCost based on the total number of words in the first word 
	# to get (word2, probability of word2 | word1)
	# TODO: To write, but not sure if it is worthwhile writing it as we still don't know what form to put

# sorted_bigramCost = sorted(bigramCost.items(), key=lambda word: len(word[1]))
# print sorted_bigramCost

# print bigramCost, len(bigramCost)
print "Finished processing"

with open(outFile, 'w') as fp: 
	json.dump(bigramCost, fp, ensure_ascii=False)


print "Finished dump"

with open(outFile) as data_file:    
    data = json.load(data_file)
    print len(data)

# test this with sample.txt before going to write the next step