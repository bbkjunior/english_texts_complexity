import json
import os

direstions = os.listdir("./check_results")
checked_ids = []
for path in direstions:
    json_path = os.path.join("./check_results",path )
    if json_path.endswith(".json"):
        with open (json_path, "r", encoding = "ISO 8859-1") as f:
            #print(json_path)
            data = json.load(f)
            for el in data:
                checked_ids.append(el['jungle_id'])
with open("checked_ids.json", 'w', encoding = "utf-8") as outfile:
        json.dump(checked_ids, outfile)