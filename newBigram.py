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

def getRealCosts(path):
    return wordsegUtil.makeLanguageModels(path)

# bigramCost, possibleFills = getRealCosts()
# print possibleFills


def run(query, bigramCost, possibleFills): 
	# query = wordsegUtil.cleanQueryLine(query)
	queryList = query.split()
	pred = states.insertVowels(queryList, bigramCost, possibleFills)
	return pred	
