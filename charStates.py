import random
import sys
import charsegUtil
# import states
import searchProblem

# Get character n-grams from corpus 

def make_character_models(path):
	one_gram = charsegUtil.make_char_nGrams(path, 1)
	two_gram = charsegUtil.make_char_nGrams(path, 2)
	three_gram = charsegUtil.make_char_nGrams(path, 3)
	four_gram = charsegUtil.make_char_nGrams(path, 4)

	# cost the ngrams

    corpus = charsegUtil.make_corpus(path)


# Define States as Vowel Insertion + Word Segmentation combination problem

# rewrite main_g.py to run dummy query through character n-gram model 



