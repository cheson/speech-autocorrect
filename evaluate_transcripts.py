import subprocess
import os

reconstructedFiles = 'reconstructed_baseline_shortened/'
    
for index in range(1, 101):
    filename = reconstructedFiles + str(index) + '_monologue.wav'

    trimCommand = ['python', os.getcwd() + '/translate_transcript.py', filename]
    subprocess.call(trimCommand)
