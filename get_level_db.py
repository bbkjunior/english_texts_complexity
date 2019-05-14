import progressbar
from calculate_level_new import get_features_from_raw_text
import pandas as pd
import time 
import json

def lower(text):
    lower_text = ''
    for word in text.split():
        w = word.lower()
        lower_text += w + ' '
    lower_text = lower_text.strip()
    return lower_text

with open('./texts/texts_lleo.json') as json_file:  
    text = []
    set_name = []
    data = json.load(json_file)
    for data_i in data:
        text.append(data_i['text'])
        set_name.append(data_i['name'])
text_level = pd.DataFrame(
    {'text': text,
     'set_name': set_name
    })
text_level['set_name'] = text_level['set_name'].apply(lower)
#text_level.head()

set_level_df = pd.read_csv("./texts/set_level.csv", sep = ",")
set_level_df['set'] = set_level_df['set'].apply(lower)
#set_level_df.head()

name_dict = pd.Series(set_level_df.level.values,index=set_level_df.set).to_dict()

level_interpret = {'Elementary':0, 'PreIntermediate':1, 'Intermediate':2, 'UpperIntermediate':3, 'Advanced':4}

def assign_level(name):
    if name in name_dict:
        return level_interpret[name_dict[name]]
    else:
        return None

text_level['level'] = text_level['set_name'].apply(assign_level)
text_level_no_nan = text_level.dropna()

text_features = []
text_ind = 0
for text in text_level_no_nan['text']:
    bar = progressbar.ProgressBar(maxval=len(text_level_no_nan['text']),
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    
    txt_ft = get_features_from_raw_text(text)
    text_features.append(txt_ft)
    
    text_ind += 1
    bar.update(text_ind)
    time.sleep(0.1)
    
features = pd.DataFrame(
    {'features': text_features,
     'level': text_level['level'],
    })
features.to_csv("text_features.csv")