#! /usr/bin/env python
# -*- coding: utf-8 -*-
from calculate_level_new import get_level_from_raw_text
import psycopg2
import json
from tqdm import tqdm
import statistics
import multiprocessing 
import time
import random

def write_response (json_file, start_index, final_index):
    file_name = './check_results/' + str(start_index) + '-' + str(final_index) +'.json'
    print("\nNOW SAVING", file_name,'\n')
    with open(file_name, 'w', encoding = "utf-8") as outfile:
        json.dump(json_file, outfile, indent=4, separators=(',', ':'),ensure_ascii=False)

conn = psycopg2.connect(dbname='pgstage', user='linguist', password='eDQGK0GCStlYlHNV', host='192.168.122.183')
interval = 100
#total pages in the base  2 262 479
level2digit = {"Beginner":'0', "Elementary/Pre-Intermediate":'1',"Intermediate":'2',"Upper-Intermediate":'3',"Advanced":'4'}
digit2level = {'0': "Beginner", '1': "Elementary/Pre-Intermediate",'2':"Intermediate",'3':"Upper-Intermediate",'4':"Advanced"}

    
def calculate_level_from_range(offset):
    texts_in_one_object = 0
    midle_calc_level = []
    current_text = {"text": '', 'jungle_id':0}
    conn.rollback()
    cursor = conn.cursor()   
    request = "SELECT jdesc ->>'page_text' AS page_text, jungle_id FROM public.content_jungle_pages LIMIT " + str(interval) + " OFFSET " + str(offset)
    print(request)
    cursor.execute(request)
    level_json = []
    check_index = 0
    #start_index = check_index
    
    for row in cursor:
        if(row[1] != current_text['jungle_id']):
            if len(current_text['text']) > 0:
                if len(midle_calc_level) > 0:
                    int_level = int(round(statistics.mean(midle_calc_level),0))
                    level = digit2level[str(int_level)]
                    midle_calc_level = []
                elif len(midle_calc_level) == 0:
                    level  = get_level_from_raw_text(current_text['text'])
                level_json.append({"jungle_id": current_text['jungle_id'], "level":level})
                print(current_text['text'], current_text['jungle_id'], "LEVEL CALCULATED AS",level, "\n")
                print("====NEW TEXT (previous texts calculations are above)====\n")
                current_text = {"text": row[0], 'jungle_id':row[1]}
                texts_in_one_object = 1
            else:
                if len(midle_calc_level) > 0:
                    int_level = int(round(statistics.mean(midle_calc_level),0))
                    level = digit2level[str(int_level)]
                    level_json.append({"jungle_id": current_text['jungle_id'], "level":level})
                    print(current_text['text'], current_text['jungle_id'], "LEVEL CALCULATED AS",level, "\n")
                    print("====NEW TEXT (previous texts calculations are above FROM LIST OF COMPLEXITIES)====\n")
                    current_text = {"text": row[0], 'jungle_id':row[1]}
                    texts_in_one_object = 1
                    midle_calc_level = []
                else:
                    print("====FIRST ENTRY====\n")#в середине текста может возникнуть если предыдущий текст был пустым
                    texts_in_one_object += 1
                    current_text['jungle_id'] = row[1]
                    current_text['text'] += ' ' + row[0]
        else:
            if texts_in_one_object <5:
                print("====ADD TEXT TO EXISTING====\n")
                current_text['text'] += ' ' + row[0]
                texts_in_one_object += 1
            else:
                print("====TOO MUCH TEXT INFO INSIDE ONE OBJECT CALCULATE AVERAGE COMPLEXITY====\n")
                level  = get_level_from_raw_text(current_text['text'])
                current_text['text'] = ''
                int_level = int(level2digit[level])
                midle_calc_level.append(int_level)
                print("CURRENT COMPLEXITY LIST IS",midle_calc_level)
                texts_in_one_object = 0
        check_index += 1
        
    #if check_index % 250 == 0 and check_index != 0:
    write_response(level_json,offset_ind, offset_ind + interval )
    level_json = []
    #start_index = check_index  

pr1=multiprocessing.Process(target=calculate_level_from_range(187500,1000000,1))
pr1.start()

calculate_level_from_range(1000000,2262500,2)


for offset_ind in tqdm(range (187500,1000000,100)):
    calculate_level_from_range(offset_ind)
