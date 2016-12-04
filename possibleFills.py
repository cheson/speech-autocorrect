import sys, json 

 
possFills = []
with open("testBigram.json") as data_file:    
    data = json.load(data_file)
    possFills = set(data)
    possFills = sorted(possFills)
    print possFills, len(data), len(possFills)

with open("possFills.json", 'w') as write_file: 
	json.dump(possFills, write_file, ensure_ascii=False)

    # print len(data)