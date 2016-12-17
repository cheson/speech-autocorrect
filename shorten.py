import subprocess
import os

reconstructedFiles = os.getcwd() + '/monologues/'
output = os.getcwd() + '/monologues_shortened/'
    

for index in range(1, 101):
    if index < 10:
        filename = '00' + str(index) + '_monologue_PCGITA.wav'
    else:
        filename = '0' + str(index) + '_monologue_PCGITA.wav'
    if index == 100:
        filename = '100_monologue_PCGITA.wav'

    trimCommand = ['sox', reconstructedFiles + filename , output + str(index) + '_monologue.wav', 'trim', str(0), str(59)]
    subprocess.call(trimCommand)
