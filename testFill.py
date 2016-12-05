import newBigram 

# gets bigramCost, possibleFills based on corpus
CORPUS_PATH = 'corpus/'
bigramCost, possibleFills = newBigram.getRealCosts(CORPUS_PATH)	


query = "l*s p*rg*s d* m*r c*r*c**r*n d* *nt*r\xc3\xa9s"#for each query == for each monologue
# vowelsToFill is a list of vowels in sequence
print query
vowelsToFill = newBigram.run(query, bigramCost, possibleFills) # need to edit run to return list of vowels
# print vowelsToFill