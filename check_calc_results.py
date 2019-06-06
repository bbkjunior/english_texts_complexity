import json
import os
from collections import OrderedDict

import argparse
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-l', '--look_for_index', type = int)
args = parser.parse_args()

direstions = os.listdir("./check_results_ordered")
level2digit =OrderedDict([("Beginner",0),("Elementary/Pre-Intermediate",0),("Intermediate",0),("Upper-Intermediate",0),("Advanced",0),("Text seems to be empty",0),("Level calculation failed",0)])
total_texts = 0
if args.look_for_index: found_list = []
for path in direstions:
    json_path = os.path.join("./check_results_ordered",path )
    if json_path.endswith(".json"):
        with open (json_path, "r") as f:
            #print(json_path)
            data = json.load(f)
            for el in data:
                if args.look_for_index:
                    if el['jungle_id'] == args.look_for_index:
                        print(json_path)
                        found_list.append((el['jungle_id'],el['level']))
                        #found_list.append(el)
                level = el['level']
                level2digit[level] +=1
                total_texts +=1
if args.look_for_index: print("collected check ind", found_list)
print("totally calculated texts ", total_texts)    
print("Absolute numbers")        
print (level2digit)
for level in level2digit.keys():
    level2digit[level] /= total_texts
    level2digit[level] = round(level2digit[level],2)
print("Normalized numbers")  
print (level2digit)
