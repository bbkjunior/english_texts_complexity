from calculate_level_new import get_level_from_raw_text
import psycopg2
import json

def write_response (json_file, start_index, final_index):
    file_name = './check_results/' + str(start_index) + '-' + str(final_index) +'.json'
    print("\nNOW SAVING", file_name,'\n')
    with open(file_name, 'w', encoding = "utf-8") as outfile:
        json.dump(json_file, outfile, indent=4, separators=(',', ':'),ensure_ascii=False)

conn = psycopg2.connect(dbname='pgstage', user='linguist', password='eDQGK0GCStlYlHNV', host='192.168.122.183')
interval = 100
#всего страниц в базе 2 262 479
current_text = {"text": '', 'jungle_id':0}
for offset_ind in range (4000,100000,interval):
    conn.rollback()
    cursor = conn.cursor()   
    request = "SELECT jdesc ->>'page_text' AS page_text, jungle_id FROM public.content_jungle_pages LIMIT " + str(interval) + " OFFSET " + str(offset_ind)
    print(request)
    cursor.execute(request)
    level_json = []
    check_index = 0
    #start_index = check_index
    for row in cursor:
        if(row[1] != current_text['jungle_id']):
            if len(current_text['text']) > 0:
                
                level  = get_level_from_raw_text(current_text['text'])
                level_json.append({"jungle_id": current_text['jungle_id'], "level":level})
                print(current_text['text'], current_text['jungle_id'], "LEVEL CALCULATED AS",level, "\n")
                print("====NEW TEXT (previous texts calculations are above)====\n")
                current_text = {"text": row[0], 'jungle_id':row[1]}
            else:
                print("====FIRST ENTRY====\n")
                current_text['jungle_id'] = row[1]
                current_text['text'] += ' ' + row[0]
        else:
            print("====ADD TEXT TO EXISTING====\n")
            current_text['text'] += ' ' + row[0]
        #print(current_text)     
        
        check_index += 1
        
    #if check_index % 250 == 0 and check_index != 0:
    write_response(level_json,offset_ind, offset_ind + interval )
    level_json = []
    #start_index = check_index  
"""
if check_index!= start_index:
    write_response(level_json,start_index, check_index )
"""