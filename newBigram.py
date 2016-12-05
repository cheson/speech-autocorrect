import util
import random
import sys
import wordsegUtil
import states

'''
TODO:
- Update wordsegutil to take in path instead of individual file 
'''

'''
This file returns BigramCost and PossibleFills as global variables
'''
######################

CORPUS_PATH = 'corpus/'

def getRealCosts():
    global _realBigramCost, _possibleFills

	if _realBigramCost is None:
	        sys.stdout.write('Training language cost functions [corpus: %s]... ' % CORPUS)
	        sys.stdout.flush()

	        _realBigramCost, _possibleFills = wordsegUtil.makeLanguageModels(CORPUS)

	        print 'Done!'
	        print ''


bigramCost, possibleFills = getRealCosts()

# def batchRun(queries):
# 	for query in query: 
# 		run(query)
		

# write function to take in queries and call batchRun 

def run(query): 
	# query = wordsegUtil.cleanQueryLine(query)
	queryList = query.split()
	pred = states.insertVowels(queryList, bigramCost, possibleFills)	

query = sys.argv[1]
print run(query)



