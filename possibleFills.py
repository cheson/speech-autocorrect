import sys, json, io, ast

 
possFills = []

with io.open("testBigram.json", 'r') as data_file:    
	data = json.load(data_file)
	data2 = ast.literal_eval(data)
	# print data2, type(data2)
	# print "printed data2"
 	# print data2
 	possFills = sorted(data2.keys())
 	print possFills, len(possFills)
    # possFills = sorted(possFills)

# print possFills, len(data), len(possFills)

with open("possFills.json", 'w') as write_file: 
	json.dump(unicode(possFills), write_file, ensure_ascii=False)