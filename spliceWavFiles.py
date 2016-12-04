import os
import string


# SETTINGS
# --------
ALIGNMENTS = os.getcwd() + '/data/alignments/pcgita_words_read_mono.frame.ali_NEW'
OUTPUT = os.getcwd() + '/data/spliced/'
ALPHABET = list(string.ascii_lowercase)
VOWELS = ['a', 'e', 'i', 'o', 'u']


# FUNCTIONS
# --------

def spliceTimeRanges(phones, letterType):
    startEndTimes = []

    i = 0
    while i < len(phones):
        # print phones[i], phones[i][0]

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
def getSpliceTimes(taskName, letterType):
    formantTimes = {}

    file = open(ALIGNMENTS, 'r')
    while (True):
        line = file.readline()
        if (not line): break
        if (line.find(taskName) >= 0):
            taskItem = line.split('PCGITA')
            filePrefix = taskItem[0] ## 001_monologue_
            phones = taskItem[1].split()

            formantTimes[filePrefix] = spliceTimeRanges(phones, letterType)

    file.close()
    return formantTimes


# FUNCTION CALLS
# --------------

monologueSpliceTimes = getSpliceTimes('monologue', ALPHABET)

# TO DO...
# Record which letter it is....
# splice .wav files...




# waveFileName
# startTime endTime
# new line
# times in milliseconds
# def outputFormantInformation(formantTimes, output):
#     keyList = sorted(list(formantTimes.keys()))
#
#     file = open(output, 'w')
#     for key in keyList:
#         toWrite = key + '\n'
#         times = formantTimes[key]
#         for time in times:
#             toWrite += str(time[0]) + ' ' + str(time[1]) + '\n'
#
#         file.write(toWrite + '\n')
#     file.close()
#
#
# def outputPerWavFormantInformation(formantTimes, outputLocation):
#     for key in formantTimes:
#
#         file = open(outputLocation + key + '.txt', 'w')
#
#         toWrite = 'Name: ' + key
#         times = formantTimes[key]
#         for time in times:
#             toWrite += ' ' + str(time[0]) + ' ' + str(time[1])
#
#         file.write(toWrite)
#         file.close()
#
# outputFormantInformation(monologueFormantTimes, OUTPUT+'monologueFormantTimes.txt')
# outputPerWavFormantInformation(monologueFormantTimes, OUTPUT)



