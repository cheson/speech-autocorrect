import newBigram 
from cutWavFiles import ProcessAlignments
from reconstruct import Reconstruct
from cutWavFiles import ALPHABET

# gets bigramCost, possibleFills based on corpus
CORPUS_PATH = 'corpus/'
bigramCost, possibleFills = newBigram.getRealCosts(CORPUS_PATH)

# processes wav files as classes
toReconstruct = Reconstruct()
alignment = ProcessAlignments()
monologueAllCutTimes = alignment.getCutTimes('monologue', ALPHABET)

queries = alignment.produceStrings(monologueAllCutTimes) # output for Gloria in string format, list of strings



# for filePrefix in queries:
#     query = queries[filePrefix] #for each query == for each monologue
#     # vowelsToFill is a list of vowels in sequence
#     print query 
#     vowelsToFill = newBigram.run(query, bigramCost, possibleFills) # need to edit run to return list of vowels
#     finalConcatWavFile = 'data/finalOutput/' + filePrefix + 'reconstructed.wav'
#     toReconstruct.fullReconstruct(filePrefix, 'monologue', vowelsToFill, finalConcatWavFile)
	
	
	eval <- wav1, wav2
	eval <- wav, transcript 

	string for 
	modifiedWav = path;
	transcriptWav = path;

	# for each query, call eval on result and its monologue transcript

query = "s* p**d*"
newBigram.run(query, bigramCost, possibleFills)