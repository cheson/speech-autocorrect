# processTranscripts: remove # comments and H_ headers so that these files can be used to process bigramCosts
# -------

import os, sys

outputFile = 'testOutputs.txt'
# filename = sys.argv[1]

path = sys.argv[1]

with open(outputFile, 'w') as fp: 
	for subdir, dirs, files in os.walk(path):
		# print files
		for filename in files:
			# remove all lines that start with H* or  # or [
			for l in open(subdir + '/' + filename).readlines():
			    if not l.startswith('#'):
			    	fp.write(l)


