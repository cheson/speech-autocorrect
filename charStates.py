import random
import sys
import charsegUtil
# import states
import searchProblem

VOWELS = 'aeiou'

# Get character n-grams from corpus 

def make_character_models(path):
	# one_gram = charsegUtil.make_char_nGrams(path, 1)
	# two_gram = charsegUtil.make_char_nGrams(path, 2)
	# three_gram = charsegUtil.make_char_nGrams(path, 3)
	# ngramCost = charsegUtil.make_nGramCost(path, 3)
	# print "made ngramCost"
	bigramCost = charsegUtil.make_bigramCost(path)
	print "made bigramCost"
	corpus = charsegUtil.make_corpus(path)
	print "made corpus"
	# four_gram = charsegUtil.make_char_nGrams(path, 4)

	# add bigramCost 

   	# return ngramCost, bigramCost, corpus
   	return bigramCost, corpus

# Define States as Vowel Insertion + Word Segmentation combination problem

# queryList is a whole string with no whitespace. 
class JointInsertionSegmentationProblem(searchProblem.SearchProblem):
	def __init__(self, query, bigramCost, possibleFills, corpus):
		self.query = query
		# self.chargramCost = chargramCost
		self.bigramCost = bigramCost
		self.possibleFills = possibleFills # save possible fills as a function to call upon 
		self.corpus = corpus

	def startState(self):
		# BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
		return ('-BEGIN-', 0)
		#raise Exception("Not implemented yet")
		# END_YOUR_CODE

	def isEnd(self, state):
		# BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
		length = len(self.query)
		return state[1] == length
		#raise Exception("Not implemented yet")
		# END_YOUR_CODE

	def succAndCost(self, state):
		# BEGIN_YOUR_CODE (our solution is 9 lines of code, but don't worry if you deviate from this)
		prevWord, currIndex = state 
		results = []

		for index in range(currIndex, len(self.query)): # for each possible segmentation of currPhrase
			wordSegment = self.query[currIndex:index+1]
			print wordSegment
			possFills = charsegUtil.make_possibleFills(wordSegment, self.corpus)

			# print possFills

			if len(possFills) > 0: 
			    for possFill in possFills:
			        results.append((possFill, (possFill,  index+1), self.bigramCost(prevWord, possFill)))
		
		print 'RESULTS: ', results
		return results
		# END_YOUR_CODE

# takes in a queryList that is the sentence including spacing. returns the filled up words
def segmentAndInsert(query, bigramCost, possibleFills, corpus):
    print 'QUERY', query

    if len(query) == 0:
        return ''

    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    final = []
    ucs = searchProblem.UniformCostSearch(verbose=0)
    for phrase in query: 
    	print 'phrase: ', phrase
    	ucs.solve(JointInsertionSegmentationProblem(phrase, bigramCost, possibleFills, corpus))
    	print 'actions: ', ucs.actions
    	final.append(ucs.actions)
    
    print final

    flattened = [val for sublist in final for val in sublist]

    # print ' '.join(final)

    # #print query, ' '.join(ucs.actions)
    return flattened
    #return query
    #raise Exception("Not implemented yet")
    # END_YOUR_CODE



path = "corpus/"
# ngramCost, bigramCost, corpus = make_character_models(path)
bigramCost, corpus = make_character_models(path)
print "made character models"
possibleFills = charsegUtil.makeInverseRemovalDictionary(corpus, VOWELS)
# print possibleFills("nstrs")
query = "n*s*tr*sv*m*s *l*pl*y*" 
print "taking in query: ", query 
# answer = segmentAndInsert(["pl*y*"], ngramCost, bigramCost, possibleFills, corpus)# 
answer = segmentAndInsert(query.split(), bigramCost, possibleFills, corpus)# 
print "final answer: ", answer
# rewrite main_g.py to run dummy query through character n-gram model 



