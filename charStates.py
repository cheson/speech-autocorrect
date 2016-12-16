import random
import sys
import charsegUtil
# import states
import searchProblem
import time
import string

# -*- coding: utf-8 -*

print sys.getdefaultencoding()

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
	def __init__(self, query, bigramCost, corpus):
		self.query = query
		# self.chargramCost = chargramCost
		self.bigramCost = bigramCost 
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
			# print wordSegment
			possFills = charsegUtil.make_possibleFills(wordSegment, self.corpus)

			# print possFills

			if len(possFills) > 0: 
			    for possFill in possFills:
			        results.append((possFill, (possFill,  index+1), self.bigramCost(prevWord, possFill)))
		
		# print 'RESULTS: ', results
		return results
		# END_YOUR_CODE

# takes in a queryList that is the sentence including spacing. returns the filled up words
def segmentAndInsert(query, bigramCost, corpus):
    # print 'QUERY', query

    if len(query) == 0:
        return ''

    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    final = []
    finalWords = []
    ucs = searchProblem.UniformCostSearch(verbose=0)
    for phrase in query: 
    	# print 'phrase: ', phrase
    	ucs.solve(JointInsertionSegmentationProblem(phrase, bigramCost, corpus))
    	# print 'actions: ', ucs.actions
    	# print 'words: ', ucs.words
    	final.append(ucs.actions)
    	# finalWords.append(ucs.words)
    
    # print final

    flattened = [val for sublist in final for val in sublist]
    print flattened
    # flattenedWords = [val for sublist in finalWords for val in sublist]
    # phrase = ' '.join(flattenedWords)
    # print "Final phrase: ", phrase
    # print ' '.join(final)

    # #print query, ' '.join(ucs.actions)
    return flattened
    #return query
    #raise Exception("Not implemented yet")
    # END_YOUR_CODE

def cleaned(query):

	def unvowel(query):
		letters = []            # make an empty list to hold the non-vowels
		for char in query:       # for each character in the word
			if char not in VOWELS:    # if the letter is not a vowel
				letters.append(char)
			else:
				letters.append('*')            # add it to the list of non-vowels
		return ''.join(letters)


	query = query.translate(None, string.punctuation)
	query = query.lower()
	print query
	return unvowel(query).split()



# path = "corpus/"
#
# start = time.time()
#
# bigramCost, corpus = make_character_models(path)
#
# charModelTime = time.time()
#
# query = "NORMALMENTE PUESACTUALMENTE EHCOMOESTOYRECIBIENDO MANUALIDADESALLADELA FUNDACIONPARKINSON DEPARKINSONME ESTOY DEDICANDOULTIMAMENTE HACERMANUALIDADES . UNAS , UNOSTRABAJOSEN , ENPUN , ENPUNTILLISMO , QUESON EN MADERA A ESO ME ESTOY DEDICANDO ULTIMAMENTE FUERA DE PUES , DE , DE , TAMBIEN VOY AL GIMNASIO A LUNES , MIERCOLES Y VIERNES , UNA HORA . PUES HAGO , EN LA QUE LE COLABORO A LA SENORA EN LOS QUEHACERES DE LA CASA CAMINO , NO MAS . ME , YO NORMALMENTE ME DESPIERTO CUATRO Y MEDIA DE LA MANANA , CUATRO Y MEDIA DE LA , CUATRO , NO , NO HASTA AHI DESPIERTO Y NO SOY CAPAZ DE DORMIR MAS PERO ME LEVANTO SEIS Y MEDIA , SIETE."
# print "Query: ", query
# print "Cleaned query: ", cleaned(query)
# # answer = segmentAndInsert(["pl*y*"], ngramCost, bigramCost, possibleFills, corpus)#
#
# beginSolveTime = time.time()
#
# answer = segmentAndInsert(cleaned(query), bigramCost, corpus)#
#
# solveTime = time.time()
#
# print "final answer: ", answer
# print "made character models in time: ", charModelTime - start
# print "Time taken to solve: ", solveTime - beginSolveTime
# rewrite main_g.py to run dummy query through character n-gram model



