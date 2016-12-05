import os
import string
import subprocess


# SETTINGS
# --------
ALIGNMENTS = os.getcwd() + '/data/alignments/pcgita_words_read_mono.frame.ali_NEW'
OUTPUT = os.getcwd() + '/data/cut/'
ALPHABET = list(string.ascii_lowercase)
VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']


class ProcessAlignments():
    def __init__(self):
        self.alignments = os.getcwd() + '/data/alignments/pcgita_words_read_mono.frame.ali_NEW'
        self.output = os.getcwd() + '/data/cut/'


    def findTimeRanges(self, phones, letterType):
        startEndTimes = []

        i = 0
        while i < len(phones):
            currentLetter = phones[i][0]

            if (currentLetter in letterType):

                startIndex = i
                nextIndex = i + 1
                while (True):
                    if (nextIndex < len(phones)):
                        nextLetter = phones[nextIndex][0]
                        if (nextLetter == currentLetter):
                            nextIndex += 1
                        else:
                            startEndTimes.append((currentLetter, startIndex * 10, nextIndex * 10))
                            i = nextIndex
                            break
                    else:
                        i = nextIndex
                        startEndTimes.append((currentLetter, startIndex * 10, nextIndex * 10))
                        break

            elif phones[i] == 'SIL':
                startIndex = i
                nextIndex = i + 1
                while (True):
                    if (nextIndex < len(phones)):
                        nextWord = phones[nextIndex]
                        if (nextWord == 'SIL'):
                            nextIndex += 1
                        else:
                            startEndTimes.append(('SIL', startIndex * 10, nextIndex * 10))
                            i = nextIndex
                            break
                    else:
                        i = nextIndex
                        startEndTimes.append(('SIL', startIndex * 10, nextIndex * 10))
                        break
            i += 1

        return startEndTimes


    # Returns a dictionary of the start and end times to splice the .wav file.
    # {'001_monologue_' : [('a', 1000, 1010), ('b', 1020, 1030), ...], '002_monologue_': [('e', 1015, 1020), ('m', 1021, 1022), ...] }
    def getCutTimes(self, taskName, letterType):
        formantTimes = {}

        file = open(ALIGNMENTS, 'r')
        while (True):
            line = file.readline()
            if (not line): break
            if (line.find(taskName) >= 0):
                taskItem = line.split('PCGITA')
                filePrefix = taskItem[0] ## 001_monologue_
                phones = taskItem[1].split()

                formantTimes[filePrefix] = self.findTimeRanges(phones, letterType)

        file.close()
        return formantTimes


    def cutWavFiles(self, cutTimeRanges):
        for filePrefix in cutTimeRanges:
            cutTimes = cutTimeRanges[filePrefix]

            for i in range(len(cutTimes)):
                timeRange = cutTimes[i]

                letter = timeRange[0]
                start = timeRange[1] * 0.001
                end = timeRange[2] * 0.001

                inputWavName = filePrefix + 'PCGITA.wav'
                outputWavName = filePrefix + str(start) + '_' + str(end) + '_' + letter + '.wav'

                soxCommand = ['sox', os.getcwd()+'/data/audio/'+inputWavName , os.getcwd()+'/data/cut/'+outputWavName, 'trim', str(start), str(abs(start-end))]
                subprocess.call(soxCommand)

        print 'Done cutting wav files'


    # Produce strings with all the vowels as '*'s
    def produceStrings(self, cutTimeRanges):
        stringsToProcess = {}

        for filePrefix in cutTimeRanges:
            toProcess = ''
            ranges = cutTimeRanges[filePrefix]

            for element in ranges:
                letter = element[0]
                if letter in VOWELS: toProcess += '*'
                else: toProcess += letter

            stringsToProcess[filePrefix] = toProcess

        print 'Done outputting strings'



alignment = ProcessAlignments()

# monologueVowelCutTimes = alignment.getCutTimes('monologue', VOWELS)
# alignment.cutWavFiles(monologueVowelCutTimes)

monologueAllCutTimes = alignment.getCutTimes('monologue', ALPHABET)
alignment.produceStrings(monologueAllCutTimes)
