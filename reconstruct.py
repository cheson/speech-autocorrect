import subprocess
import os
import string
from cutWavFiles import ProcessAlignments
import charStates, charsegUtil

ALPHABET = list(string.ascii_lowercase)
VOWELS = ['a', 'e', 'i', 'o', 'u'] # 'y' as vowel?

class Reconstruct():
    def __init__(self):
        self.originalsLocation = os.getcwd() + '/data/audio/'
        self.temporaryOutput = os.getcwd() + '/data/'
        self.reconstructedFiles = os.getcwd() + '/data/reconstructed/'
        self.replacementVowelLocation = os.getcwd() + '/data/perfect_vowels/'
        self.vowels = ['a', 'e', 'i', 'o', 'u'] # 'y' as a vowel?
    

    def reconstruct(self, originalWavFile, startPoint, endPoint, replacement, finalConcatWav):
        # trim the original audio file from startPoint to endPoint
        # store output in self.temporaryWav
        temporaryWav = self.temporaryOutput + 'temp.wav'
        temporaryWav2 = self.temporaryOutput + 'temp2.wav'
        temporaryWav3 = self.temporaryOutput + 'temp3.wav'
        createTemp2Wav = ['sox', self.originalsLocation + originalWavFile, temporaryWav2,
                          'trim', str(0.0), str(0.0)]
        subprocess.call(createTemp2Wav)

        trimCommand = ['sox', self.originalsLocation+originalWavFile, temporaryWav, 'trim', str(startPoint), str(abs(startPoint-endPoint))]
        subprocess.call(trimCommand)

        concatCommand = ['sox', temporaryWav, replacement, temporaryWav2]
        subprocess.call(concatCommand)

        createTemp3Wav = ['sox', self.reconstructedFiles + finalConcatWav, temporaryWav3, 'trim', str(0.0)]
        subprocess.call(createTemp3Wav)

        concatCommand = ['sox', temporaryWav3, temporaryWav2, self.reconstructedFiles+finalConcatWav]
        subprocess.call(concatCommand)

        # concatCommand = ['sox', temporaryWav3, temporaryWav, self.reconstructedFiles + finalConcatWav]
        # subprocess.call(concatCommand)

        os.remove(self.temporaryOutput+'temp.wav')
        os.remove(self.temporaryOutput+'temp2.wav')
        os.remove(self.temporaryOutput+'temp3.wav')
        
        
    def getReplacementWav(self, vowel):
        return self.replacementVowelLocation + vowel + '.wav'
        # perfectVowel = self.replacementVowelLocation + vowel +'.wav'

    
    # Repeatedly call reconstruct on the correct start and end points 
    # (corresponding to the places surrounding what we need to replace). 
    # H*L*
    # [O, A]
    def fullReconstruct(self, filePrefix, task, replacements, finalConcatWav):
        originalWavFile = filePrefix + 'PCGITA.wav'

        # {'001_monologue_': [('a', 1000, 1020), ('e', 1021, 1024)]}
        alignment = ProcessAlignments()
        oldVowelsStartEnd = alignment.getCutTimes(task, self.vowels)[filePrefix]
        vowelsStartEnd = []

        # remove SIL because reconstruct only cares about vowels
        for item in oldVowelsStartEnd:
            if not item[0] == 'SIL':
                vowelsStartEnd.append(item)

        assert len(vowelsStartEnd) == len(replacements)

        createFinalWav = ['sox', self.originalsLocation+originalWavFile, self.reconstructedFiles+finalConcatWav, 'trim', str(0.0), str(0.0)]
        subprocess.call(createFinalWav)

        currEnd = 0.0

        for i in range(len(replacements)):
            vowel = replacements[i]
            startEnd = vowelsStartEnd[i]
            start = startEnd[1] * 0.001  # to seconds
            end = startEnd[2] * 0.001  # to seconds

            replacementWav = self.getReplacementWav(vowel)

            self.reconstruct(originalWavFile, currEnd, start, replacementWav, finalConcatWav)

            currEnd = end



# correct = []
# for item in vowelsStartEnd:
#     if not item[0] == 'SIL':
#         correct.append(item[0])
# print correct

path = 'corpus/'
bigramCost, corpus = charStates.make_character_models(path)


alignment = ProcessAlignments()
vowelsStartEnd = alignment.getCutTimes('monologue', VOWELS)['001_monologue_']

monologueAllCutTimes = alignment.getCutTimes('monologue', ALPHABET)
queries = alignment.produceStrings(monologueAllCutTimes)
query = queries['001_monologue_']
print query

answer = charStates.segmentAndInsert(query, bigramCost, corpus)

reconstruct = Reconstruct()
reconstruct.fullReconstruct('001_monologue_', 'monologue', answer, 'reconstructed_001_monologue.wav')