import subprocess
import os
import string
from cutWavFiles import ProcessAlignments
import charStates, charsegUtil
import time

ALPHABET = list(string.ascii_lowercase)
VOWELS = ['a', 'e', 'i', 'o', 'u', 'w'] # 'y' as vowel?
genderFile = "gender.txt"

class Reconstruct():
    def __init__(self):
        self.originalsLocation = os.getcwd() + '/data/audio/'
        self.temporaryOutput = os.getcwd() + '/data/'
        self.reconstructedFiles = os.getcwd() + '/data/reconstructedGender/'
        self.replacementVowelLocation = os.getcwd() + '/PerfectVowels/'
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'w'] # 'y' as a vowel?

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
        
        
    def getReplacementWav(self, vowel, gender):
        return self.replacementVowelLocation + gender + vowel + '.wav'
        # return self.replacementVowelLocation + vowel +'.wav'


    # Repeatedly call reconstruct on the correct start and end points 
    # (corresponding to the places surrounding what we need to replace). 
    # H*L*
    # [O, A]
    def fullReconstruct(self, filePrefix, task, replacements, finalConcatWav, gender):
        originalWavFile = filePrefix + 'PCGITA.wav'

        # {'001_monologue_': [('a', 1000, 1020), ('e', 1021, 1024)]}
        alignment = ProcessAlignments()
        oldVowelsStartEnd = alignment.getCutTimes(task, self.vowels)[filePrefix]
        vowelsStartEnd = []

        # remove SIL because reconstruct only cares about vowels
        for item in oldVowelsStartEnd:
            if not item[0] == 'SIL':
                vowelsStartEnd.append(item)

        print len(vowelsStartEnd)
        print len(replacements)

        assert len(vowelsStartEnd) == len(replacements)

        createFinalWav = ['sox', self.originalsLocation+originalWavFile, self.reconstructedFiles+finalConcatWav, 'trim', str(0.0), str(0.0)]
        subprocess.call(createFinalWav)

        currEnd = 0.0

        for i in range(len(replacements)):
            vowel = replacements[i]
            startEnd = vowelsStartEnd[i]
            start = startEnd[1] * 0.001  # to seconds
            end = startEnd[2] * 0.001  # to seconds

            replacementWav = self.getReplacementWav(vowel, gender)

            self.reconstruct(originalWavFile, currEnd, start, replacementWav, finalConcatWav)

            currEnd = end


def getGenders():
    result = {}
    with open(genderFile, 'r') as f:
        for line in f:
            person, gender = line.split()
            key = person + '_monologue_'
            result[key] = gender

        f.close()

    print result
    return result


# correct = []
# for item in vowelsStartEnd:
#     if not item[0] == 'SIL':
#         correct.append(item[0])
# print correct

path = 'corpus/'
bigramCost, corpus = charStates.make_character_models(path)

monologueGenders = getGenders()

alignment = ProcessAlignments()
monologueALLCutTimes = alignment.getCutTimes('monologue', ALPHABET)
queries = alignment.produceStrings(monologueALLCutTimes)

# filePrefix = '001_monologue_'
for filePrefix in queries:
    print 'working on ', filePrefix

    query = queries[filePrefix]
    print query

    reconstructStart = time.time()
    answer = charStates.segmentAndInsert(query.split(), bigramCost, corpus)
    reconstructEnd = time.time()
    print 'segmented and inserted in time: ', reconstructEnd - reconstructStart
    print answer

    gender = monologueGenders[filePrefix]

    reconstruct = Reconstruct()
    reconstruct.fullReconstruct(filePrefix, 'monologue', answer, 'reconstructed_'+filePrefix+'.wav', gender)

    print 'done reconstructing ', filePrefix





# ---------------------------------------------------------------------------------
# query = queries['001_monologue_']
# print query
#
# vowelsStartEnd = alignment.getCutTimes('monologue', VOWELS)['001_monologue_']
#
# vowelCount = 0
# for item in vowelsStartEnd:
#     if not item[0] == 'SIL':
#         vowelCount += 1
#
# print vowelsStartEnd
# print vowelCount
#
# queryCount = 0
# for char in query:
#     if char == '*': queryCount += 1
#
# print query
# print queryCount
#
#
# # query = "NORMALMENTE PUESACTUALMENTE EHCOMOESTOYRECIBIENDO MANUALIDADESALLADELA FUNDACIONPARKINSON DEPARKINSONME ESTOY DEDICANDOULTIMAMENTE HACERMANUALIDADES . UNAS , UNOSTRABAJOSEN , ENPUN , ENPUNTILLISMO , QUESON EN MADERA A ESO ME ESTOY DEDICANDO ULTIMAMENTE FUERA DE PUES , DE , DE , TAMBIEN VOY AL GIMNASIO A LUNES , MIERCOLES Y VIERNES , UNA HORA . PUES HAGO , EN LA QUE LE COLABORO A LA SENORA EN LOS QUEHACERES DE LA CASA CAMINO , NO MAS . ME , YO NORMALMENTE ME DESPIERTO CUATRO Y MEDIA DE LA MANANA , CUATRO Y MEDIA DE LA , CUATRO , NO , NO HASTA AHI DESPIERTO Y NO SOY CAPAZ DE DORMIR MAS PERO ME LEVANTO SEIS Y MEDIA , SIETE."
#
# path = 'corpus/'
# bigramCost, corpus = charStates.make_character_models(path)
#
# reconstructStart = time.time()
#
# answer = charStates.segmentAndInsert(query.split(), bigramCost, corpus)
# # answer = charStates.segmentAndInsert(charStates.cleaned(query), bigramCost, corpus)#
#
# reconstructEnd = time.time()
#
# print 'segmented and inserted in time: ', reconstructEnd - reconstructStart
#
# print answer
#
# reconstruct = Reconstruct()
# reconstruct.fullReconstruct('001_monologue_', 'monologue', answer, 'reconstructed_001_monologue.wav')
#
# print 'done reconstructing'
