# import newBigram 
# from cutWavFiles import ProcessAlignments
# from reconstruct import Reconstruct
# from cutWavFiles import ALPHABET

# gets bigramCost, possibleFills based on corpus
# CORPUS_PATH = 'corpus/'
# bigramCost, possibleFills = newBigram.getRealCosts(CORPUS_PATH)
TRANSCRIPT_FILE = 'AllText.txt'
####################################

filePrefix = "096_SENT08_PCGITA"
transcript = ""
with open(TRANSCRIPT_FILE) as f:
	for line in f:
		if line.find(filePrefix) == 0:
		     transcript = line
		     transcript = transcript.replace(filePrefix, '')

print transcript