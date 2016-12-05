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

global _realBigramCost, _possibleFills


def getRealCosts():
    print 'Done!'
    return wordsegUtil.makeLanguageModels(CORPUS_PATH)

	        


bigramCost, possibleFills = getRealCosts()
print possibleFills

# def batchRun(queries):
# 	for query in query: 
# 		run(query)
		

# write function to take in queries and call batchRun 

def run(query): 
	# query = wordsegUtil.cleanQueryLine(query)
	queryList = query.split()
	pred = states.insertVowels(queryList, bigramCost, possibleFills)
	return pred	

query = sys.argv[1]
print run(query)



