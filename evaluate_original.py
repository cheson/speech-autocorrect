import subprocess
import os

fileloc = 'monologues_shortened/'
    
for index in range(22, 101):
    filename = fileloc + str(index) + '_monologue.wav'

    trimCommand = ['python', os.getcwd() + '/translate_original.py', filename]

    subprocess.call(trimCommand)
