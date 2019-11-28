import re
with open("new_phrasal.txt", 'r') as f:
    for line in f.readlines():
        result = re.findall('[a-zA-Z ]*', line)
        print (result[0].strip())
        #print(line.split("—")[0].strip())