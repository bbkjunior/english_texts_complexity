import json
import os

direstions = os.listdir("./check_results")
level2digit = {"Beginner":0, "Elementary/Pre-Intermediate":0,"Intermediate":0,"Upper-Intermediate":0,"Advanced":0,"Text seems to be empty":0}
total_texts = 0
for path in direstions:
    json_path = os.path.join("./check_results",path )
    if json_path.endswith(".json"):
        with open (json_path, "r", encoding = "ISO 8859-1") as f:
            #print(json_path)
            data = json.load(f)
            for el in data:
                level = el['level']
                level2digit[level] +=1
                total_texts +=1
print("totally calculated texts ", total_texts)    
print("Absolute numbers")        
print (level2digit)
for level in level2digit.keys():
    level2digit[level] /= total_texts
    level2digit[level] = round(level2digit[level],2)
print("Normalized numbers")  
print (level2digit)