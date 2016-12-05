import newBigram 
from cutWavFiles import ProcessAlignments
from reconstruct import Reconstruct
from cutWavFiles import ALPHABET

# gets bigramCost, possibleFills based on corpus
CORPUS_PATH = 'corpus/'
TRANSCRIPT_FILE = 'data/AllText.txt'

bigramCost, possibleFills = newBigram.getRealCosts(CORPUS_PATH)

# processes wav files as classes
toReconstruct = Reconstruct()
alignment = ProcessAlignments()
monologueAllCutTimes = alignment.getCutTimes('monologue', ALPHABET)

queries = alignment.produceStrings(monologueAllCutTimes) # output for Gloria in string format, list of strings



for filePrefix in queries:
    query = queries[filePrefix] #for each query == for each monologue
    # vowelsToFill is a list of vowels in sequence
    print query 
    vowelsToFill = newBigram.run(query, bigramCost, possibleFills) # need to edit run to return list of vowels
    finalConcatWavFile = 'data/finalOutput/' + filePrefix + 'reconstructed.wav'
    toReconstruct.fullReconstruct(filePrefix, 'monologue', vowelsToFill, finalConcatWavFile)
	
	transcript = ''
	with open(TRANSCRIPT_FILE) as f:
	for line in f:
		if line.find(filePrefix) == 0:
		     transcript = line
		     transcript = transcript.replace(filePrefix, '')

	#modifiedWav = filePrefix + modifiedWavLocation

	#call eval(modifiedWav, transcript)
	#os.system('call eval') eval(inputWav, transcript, filePrefix)
