import subprocess


class Reconstruct():
    def __init__(self):
        self.originalsLocation = os.getcwd() + '/data/audio/'
        self.temporaryOutput = os.getcwd() + '/data/temporary/'
        self.reconstructedFiles = os.getcwd() + '/data/reconstructed/'
        self.temporaryWav = self.temporaryOutput + 'temp.wav'
        self.tempConcatWav = self.temporaryOutput + 'concat.wav'
        
        self.replacementVowelLocation = os.getcwd() + ## FILL THIS IN!! ##
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    
    
    def reconstruct(self, originalWavFile, startPoint, endPoint, replacement, finalConcatWav):
        # trim the original audio file from startPoint to endPoint
        # store output in self.temporaryWav
        trimCommand = ['sox', self.originalsLocation+originalWavFile , self.temporaryWav, 'trim', str(startPoint), str(abs(startPoint-endPoint))]
        subprocess.call(trimCommand)
        
        concatCommand = ['sox', self.temporaryWav, replacement, self.tempConcatWav]
        subprocess.call(concatCommand)
        
        concatCommand = ['sox', finalConcatWav, self.tempConcatWav, finalConcatWav]
        subprocess.call(concatCommand)
        
        
    def getReplacementWav(vowel):
        ## FILL THIS IN!!! ##
        # look at all the files in the directory 
        
    
    # Repeatedly call reconstruct on the correct start and end points 
    # (corresponding to the places surrounding what we need to replace). 
    # H*L*
    # [O, A]
    def fullReconstruct(self, filePrefix, task, replacements, finalConcatWav):    
        
        # {'001_monologue_': [('a', 1000, 1020), ('e', 1021, 1024)]}
        alignment = ProcessAlignments()
        vowelsStartEnd = alignment.getCutTimes(task, self.vowels)[filePrefix]

        currEnd = 0.0
        
        for i in range(len(replacements)):
            vowel = replacements[i]
            replacementWav = getReplacementWav(vowel)
            
            startEnd = vowelsStartEnd[i]
            start = startEnd[1]*0.001 # to seconds
            end = startEnd[2]*0.001 # to seconds
            
            originalWavFile = '/data/audio/' + filePrefix + 'PCGITA.wav'

            reconstruct(originalWavFile, currEnd, start, replacement, finalConcatWav)
            
            currEnd = end