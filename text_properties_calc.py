from ud_class import Model
from vocabulary import final_basic_vocabulary, phrasal_list_EASY, phrasal_list_big
from grammar_properties import get_non_verb_phrase_properties, get_verb_phrase_properties 
from collections import OrderedDict
import copy

"""
import argparse
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

DEBUG = False
if (args.debug ):
    DEBUG = True"""
DEBUG = False
model = Model('./UDPIPE/english-ud-2.0-170801.udpipe')

def get_conllu(text_line, model, print_output = DEBUG):
    sentences = model.tokenize(text_line)
    for s in sentences:
        model.tag(s)
        model.parse(s)
    conllu = model.write(sentences, "conllu")
    if (print_output):
        for line in conllu.split('\n'):
            if line:
                if line[0].isdigit():
                    print(line.split('\t'))
                else:
                    print(line)
    return conllu
    
def get_conllu_text_map(conllu_parsed_object):
    conllu_text_map = []
    conllu_sentence_map = []
    for line in conllu_parsed_object.split('\n'):
        if line :
            if line[0].isdigit():
                #print(line.split('\t'))
                split_items = line.split('\t')
                if split_items[3] != "PUNCT":
                    conllu_sentence_map.append(split_items)
            else:
                if(len(conllu_sentence_map) > 0):
                    conllu_text_map.append(conllu_sentence_map)
                    conllu_sentence_map = []   
                    #print("appended")
    if(len(conllu_sentence_map) > 0):
        conllu_text_map.append(conllu_sentence_map)
    return conllu_text_map
    
    
def create_map(conllu_map, tf_idf_dict, apply_tf_idf = True):
    text_map = []
    sentence_ind = 0
    for sentence in conllu_map:
        sentence_map = []
        real_index = 1
        for word in sentence: 
            weight = OrderedDict([("word", word[1]),("lemma",word[2]), ("vocabulary_prop",(OrderedDict([("vocab_importane", 0),("nominal_index",word[0])])))])
            
            lemma_lower = word[2].lower()
            if (apply_tf_idf):
                if (lemma_lower in tf_idf_dict):
                    tf_idf_i = tf_idf_dict[lemma_lower][sentence_ind]
                    if(word[3] not in pos_exclude_list):
                        weight['vocabulary_prop']["vocab_importane"] = tf_idf_i
                    elif(tf_idf_i > 0 ):
                        #print(word)
                        weight['vocabulary_prop']["vocab_importane"] = tf_idf_i * 0.5
            sentence_map.append(weight)
        text_map.append(sentence_map)
        sentence_ind += 1
    return text_map
    
def vocabulary_analysis(text_map_input, dictionary, debug = False):
    text_map = copy.deepcopy(text_map_input)
    a1_vocab = []
    other_vocab = []
    a1_weight = 0
    other_weight = 0
    for sentence in text_map:
        for word in sentence:
            low_lemma = word['lemma'].lower()
            low_lemma_clean = ''
            for char in low_lemma:
                if char not in full_punctuation:
                    low_lemma_clean += char
            
            if(low_lemma_clean not in dictionary):
                other_vocab.append((low_lemma_clean,word['vocabulary_prop']['vocab_importane']))
                other_weight += word['vocabulary_prop']['vocab_importane']
            else:
                a1_vocab.append((low_lemma_clean,word['vocabulary_prop']['vocab_importane']))
                a1_weight += word['vocabulary_prop']['vocab_importane']
    if debug:
        print(a1_weight, a1_vocab)
        print("OTHER VOCAB")
        print(other_weight, other_vocab)
            
#vocabulary_analysis(text_map_ex, final_basic_vocabulary)      

def build_subtree_branch(head_word_nominal_index, pos_word_dict,verb_phrases_dict, word_leave):
    if (int(head_word_nominal_index)!= 0):
        current_head_word = pos_word_dict[head_word_nominal_index][0]
        current_head_pos = pos_word_dict[head_word_nominal_index][1][1]
        #print("current_head_word",pos_word_dict[head_word_nominal_index])
        if(current_head_word in verb_phrases_dict):
            verb_phrases_dict[current_head_word].append(word_leave)
        else:
            verb_phrases_dict[current_head_word] = []
            verb_phrases_dict[current_head_word].append(word_leave)     


def grammar_analysis(conllu_map,text_map_input, show_trees = DEBUG, show_log = DEBUG):
    assert len(conllu_map) == len(text_map_input) #sentences count is equal
    text_map = copy.deepcopy(text_map_input)
    
    for sentence_conllu, text_map_sentence in zip(conllu_map,text_map):
        #СОБИРАЕМ СПИСОК СВАОЙСТВ ВСЕХ СЛОВ ПРЕДЛОЖЕНИЯ ДЛЯ ПОСЛЕДУЮЩЕГО ОБРАЩЕНИЯ
        pos_word_dict = {}
        for pos_word in sentence_conllu:
            pos_word_dict[pos_word[0]] = (pos_word[0]+'_'+pos_word[1]+'_'+pos_word[2], pos_word[2:])
        
        #print("POS", pos_word_dict)# словарь "номинальный индекс слова" (номинальный-индекс_слово,  остальные conllu based свойства)
        grammar_properties_log = {}
        vocab_properties_log = {}
        #СТРОИМ ПОДДЕРЕВЬЯ ГЛАГОЛЬНЫХ ГРУПП И СРАЗУ СМОТРИМ ЛИНЕЙНЫЕ СВОЙСТВА
        verb_phrases_dict = {}#словарь "индекс_слово(глагол в верштне)" [список conllu based свойств зависимых эл-тов]
        non_verb_phrases_dict = {}

        for word_leave_index in range(len(sentence_conllu)):
            if sentence_conllu[word_leave_index][3] == "VERB":
                for word_leave_pv in range(min(len(sentence_conllu), word_leave_index + 3)):
                    potential_phrasal_verb = sentence_conllu[word_leave_index][2] + ' ' + sentence_conllu[word_leave_pv][2]
                    first_index = sentence_conllu[word_leave_index][0]
                    second_index = sentence_conllu[word_leave_pv][0]
                    if( potential_phrasal_verb in  phrasal_list_EASY):
                        #print("EASY PV DETECTED")
                        if abs(int(first_index) - int(second_index)) > 2:
                            vocab_properties_log[first_index] = "dist_easy_phrasal_verb"
                            vocab_properties_log[second_index] = "dist_easy_phrasal_verb"
                        else:
                            vocab_properties_log[first_index] = "easy_phrasal_verb"
                            vocab_properties_log[second_index] = "easy_phrasal_verb"
                    elif(potential_phrasal_verb in phrasal_list_big):
                        if abs(int(first_index) - int(second_index)) > 2:
                            vocab_properties_log[first_index] = "dist_phrasal_verb"
                            vocab_properties_log[second_index] = "dist_phrasal_verb"
                        else:
                            vocab_properties_log[first_index] = "phrasal_verb"
                            vocab_properties_log[second_index] = "phrasal_verb"
        
        for word_leave in sentence_conllu: 
            #if word_leave[2] == "there": there_is_are = True
            #if word_leave[1].lower() in be_list and there_is_are"
            #print(word_leave[1], "head_word_nominal_index =", word_leave[6])
            if (int(word_leave[6]) != 0):
                #print(pos_word_dict[word_leave[6]],pos_word_dict[word_leave[6]][1][1])
                if(pos_word_dict[word_leave[6]][1][1] != "VERB"):
                    build_subtree_branch(word_leave[6], pos_word_dict, non_verb_phrases_dict, word_leave)
                else:
                    build_subtree_branch(word_leave[6], pos_word_dict, verb_phrases_dict, word_leave)

        if (show_trees):
            print("VERB SUBTREES")
            for key, value in verb_phrases_dict.items():
                print(key)
                for el in value:
                    print(el)
                print("==========")
        if (len(list(verb_phrases_dict.keys()))>0):
            get_verb_phrase_properties(verb_phrases_dict, grammar_properties_log,pos_word_dict,vocab_properties_log)
        
        if (show_trees):
            print("NON-VERB SUBTREES")
            for key, value in non_verb_phrases_dict.items():
                print(key)
                for el in value:
                    print(el)
                print("==========")
        if (len(list(non_verb_phrases_dict.keys()))>0):
            get_non_verb_phrase_properties(non_verb_phrases_dict, grammar_properties_log,pos_word_dict,vocab_properties_log)
        
                
        if show_log:
            print("grammar_properties_log", grammar_properties_log) 
            print("vocab_properties_log", vocab_properties_log)  
        
        if ("if_pres" in grammar_properties_log):
            future = False
            present = False  
            for key, val in grammar_properties_log.items():
                if (key != "if_pres"):
                    if(val == "PresSimp"):
                        present = True
                    elif("Fut" in val):
                        future = True
            if future and present:
                grammar_properties_log[grammar_properties_log["if_pres"]] = "FirstCond"
            elif not future and present:
                grammar_properties_log[grammar_properties_log["if_pres"]] = "ZeroCond"
            if show_log: print("grammar_properties_log CHANGED", grammar_properties_log)  
        
        if ("if_past" in grammar_properties_log and "would_Vinf" in grammar_properties_log):
            grammar_properties_log[grammar_properties_log["if_past"]] = "SecondCond"
            if show_log: print("grammar_properties_log CHANGED", grammar_properties_log) 
        if ("if_past_perf" in grammar_properties_log and "would_have_V3" in grammar_properties_log):
            grammar_properties_log[grammar_properties_log["if_past_perf"]] = "ThirdCond"
            if show_log: print("grammar_properties_log CHANGED", grammar_properties_log)
            
        for map_word in text_map_sentence:
            word_index = map_word['vocabulary_prop']['nominal_index']
            if (str(word_index) in grammar_properties_log):
                map_word['grammar_prop'] = grammar_properties_log[word_index]
            if (str(word_index) in vocab_properties_log):
                map_word['vocabulary_prop']['supp_properties'] = vocab_properties_log[word_index]
            
                
    return text_map, grammar_properties_log, vocab_properties_log
        
#grammar_analysis(conllu_text_map_ex,text_map_dep)

    
def get_map(text_line,model):
    conllu = get_conllu(text_line, model, print_output = DEBUG)
    conllu_text_map = get_conllu_text_map(conllu)
    #print(conllu_text_map)
    
    tfidf = False
    if tfidf:
        lemm_sentences = lemmatize_from_udmap(conllu_text_map)
        tf_idf_dict = get_tf_idf_dict (lemm_sentences)
    else:
        tf_idf_dict = None
    
    text_map = create_map(conllu_text_map, tf_idf_dict, apply_tf_idf = False)
    
    #vocabulary_analysis(text_map_dep, final_basic_vocabulary)
    text_analysis_map, grammar_properties_log, vocab_properties_log = grammar_analysis(conllu_text_map, text_map)
    
    return text_analysis_map, grammar_properties_log, vocab_properties_log
    
   
if DEBUG:
    map, grammar_properties_log, vocab_properties_log = get_map("There will have been a lot of cars in the garage", model)
    for word in map[0]:
        print (word,"\n")
#get_map("I like going there", model) Gerund example
#get_map("The cat will be there", model)
#get_map("Mrs Scolefield  has really-really liked going there", model)# has to root
#get_map("Mr. Scolefield is going there", model)
#Is he going there""He is a cat" --- на этом примере Tense не отрабатывает --- решение - посылать на еще одну обработку без корня
#Had I gone there --- Had уходит в корень - время определяется неправильно


        
    


    
    
            

