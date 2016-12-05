import sys, json, ast, io

# with open("possFills.json") as data_file:    
#     data = json.load(data_file)
#     print data

with io.open("possFills.json", 'r') as data_file:    
	data = json.load(data_file)
	print type(data)
	data2 = sorted(ast.literal_eval(data))
	print data2, type(data2), len(data2)