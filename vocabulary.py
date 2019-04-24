#UPLOAD BASICAL PHRASAL VERBS
phrasal_list_EASY = []
with open("./materials/phrasal_verbs_easy", "r") as pv_doc:
    for pv in pv_doc:
        phrasal_list_EASY.append(pv[:-1])
		
#UPLOAD ALL PHRASAL VERBS
phrasal_list_big = []
with open("./materials/phrasal_verbs.txt", "r") as pv_doc:
    for pv in pv_doc:
        phrasal_list_big.append(pv[:-1])

#UPLOAD BASIC VOCABULARY	
basic_vocabulary = []
with open("./materials/A1_vocab_processed.txt", "r",encoding = "ISO-8859-1") as voc:
    for word in voc.readlines():
        basic_vocabulary.append(word[:-1].lower())
#basic_vocabulary = set(basic_vocabulary)
#basic_vocabulary

adjectives = []
with open("./materials/common_adj.txt", "r") as common_adj:
    for word in common_adj.readlines():
        adjectives.append(word[:-1].lower())
        
common_uncountable = []
with open("./materials/common_unountable_manually_filtered.txt", "r") as common_unctbl:
    for word in common_unctbl.readlines():
        common_uncountable.append(word[:-1].lower())

countries = []
with open("./materials/countries.txt", "r") as cntr:
    for word in cntr.readlines():
        countries.append(word[:-1].lower())

names = []
with open("./materials/names.txt", "r") as names_file:
    for word in names_file.readlines():
        names.append(word[:-1].lower())
        
#print(len(basic_vocabulary), len(adjectives), len(common_uncountable), len(countries), len(countries), len(names))
final_basic_vocabulary = basic_vocabulary
final_basic_vocabulary.extend(adjectives)
final_basic_vocabulary.extend(common_uncountable)
final_basic_vocabulary.extend(countries)
final_basic_vocabulary.extend(names)
#print(len(final_basic_vocabulary))
final_basic_vocabulary = set(final_basic_vocabulary)