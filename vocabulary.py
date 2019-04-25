#UPLOAD BASICAL PHRASAL VERBS
"""
phrasal_list_EASY = []
with open("./materials/phrasal_verbs_easy", "r") as pv_doc:
    for pv in pv_doc:
        phrasal_list_EASY.append(pv[:-1])"""
		
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
word_to_find = None
if word_to_find:
    print (word_to_find)
A2 = []
with open("./materials/A2_vocab_processed.txt", "r") as voc:
    for word in voc.readlines():
        if word_to_find:
                if word_to_find in word:
                    print (word, 'A2')
        A2.append(word[:-1].lower())

if word_to_find:
    print(len(A2))
A2 = set(A2) - final_basic_vocabulary
if word_to_find:
    print(len(A2))
    print(word_to_find in A2)

B1 = []
with open("./materials/B1_vocab_processed.txt", "r") as voc:
    for word in voc.readlines():
        if word_to_find:
            if word_to_find in word:
                print (word, 'B1')
        B1.append(word[:-1].lower())
if word_to_find:
    print(len(B1))
B1 = set(B1) - final_basic_vocabulary
if word_to_find:
    print(len(B1))
    print(word_to_find in B1)

B2 = []
with open("./materials/B2_vocab_processed.txt", "r") as voc:
    for word in voc.readlines():
        if word_to_find:
            if word_to_find in word:
                print (word, 'B2')
        B2.append(word[:-1].lower())

if word_to_find:
    print(len(B2))
B2 = set(B2) - final_basic_vocabulary
if word_to_find:
    print(len(B2))
    print(word_to_find in B2)

C = []
with open("./materials/C_vocab_processed.txt", "r") as voc:
    for word in voc.readlines():
        if word_to_find:
            if word_to_find in word:
                print (word, 'C')
        C.append(word[:-1].lower())
if word_to_find:
    print(len(B2))
C = set(C) - final_basic_vocabulary
if word_to_find:
    print(len(B2))
    print(word_to_find in C)

cefr_dictionary = {'A1':final_basic_vocabulary, 'A2':A2, 'B1':B1,'B2':B2,'C':C}
