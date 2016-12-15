import newBigram 
from cutWavFiles import ProcessAlignments
from reconstruct import Reconstruct
from cutWavFiles import ALPHABET
import evaluate
import  random
import wordsegUtil


# gets bigramCost, possibleFills based on corpus
CORPUS_PATH = 'corpus/'
bigramCost, possibleFills = newBigram.getRealCosts(CORPUS_PATH)
TRANSCRIPT_FILE = 'data/AllText.txt'

# processes wav files as classes
toReconstruct = Reconstruct()
alignment = ProcessAlignments()
monologueAllCutTimes = alignment.getCutTimes('monologue', ALPHABET)

# totalPercentageChange = 0
# totalNumQueries = 0 
# totalImprovements = 0

queries = alignment.produceStrings(monologueAllCutTimes) # output for Gloria in string format, list of strings


def fillQuery(query, vowelsToFill): 
	result = ""
	vowelIndex = 0
	for word in query: 
		for ch in word:
			if ch == '*': 
				replaceV = vowelsToFill[vowelIndex]
				if replaceV == '*':
					replaceV = random.choice('aeiouy')
				vowelIndex += 1
				result += replaceV
			else: 
				result += ch 

	return result


for filePrefix in queries:
    query = queries[filePrefix] #for each query == for each monologue
    # vowelsToFill is a list of vowels in sequence
    # print query 
    vowelsToFill = newBigram.run(query, bigramCost, possibleFills) # need to edit run to return list of vowels
    modifiedStr = fillQuery(query, vowelsToFill)

    """
    Find way to compare similarity to transcript
    """

    # finalConcatWavFile = 'data/finalOutput/' + filePrefix + 'reconstructed.wav'
    # toReconstruct.fullReconstruct(filePrefix, 'monologue', vowelsToFill, finalConcatWavFile)
	
	
	# eval <- wav1, wav2
	# eval <- wav, transcript 

	# extract line with same starting filePrefix in data/AllText.txt 
	transcript = ""
	with open(TRANSCRIPT_FILE) as f:
    for line in f:
        if line.find(filePrefix) == 0:
             transcript = line
             transcript = transcript.replace(filePrefix, '')
             transcript = wordsegUtil.cleanLine(transcript)

    score = 0
    for i in range(len(transcript)): 
    	for j in range(len(transcript[j]))
    	if modifiedStr[i][j] == transcript[i][j]: score += 1

    score = score * 1.0 / len(transcript)
   	print score 


    
#     originalWavFile = 'data/audio/' + filePrefix + '.wav'
#     origScore = evaluate.main(originalWavFile, transcript, filePrefix)
#     modifiedScore = evaluate.main(finalConcatWavFile, transcript, filePrefix)
#     print "Original score: " + origScore + "; Modified score: " + modifiedScore
#     percentageChange = (modifiedScore - origScore) * 1.0 / origScore * 100
#     improvement = (percentageChange > 0)
#     print "Percentage improvement: " + percentageChange + "; Improvement: " + improvement

#     totalPercentageChange += percentageChange
#     if improvement == 1:
#     	totalImprovements += 1
#     totalNumQueries += 1

# avPercentageChange = totalPercentageChange * 1.0 / totalNumQueries
# avImprovement = totalImprovements * 1.0 / totalNumQueries 

# print "avPercentageChange: " + avPercentageChange + "; avImprovement: " + avImprovement


# 	# string for 
# 	modifiedWav = path;
# 	transcriptWav = path;

	# for each query, call eval on result and its monologue transcript

# query = "s* p**d*"
# newBigram.run(query, bigramCost, possibleFills)