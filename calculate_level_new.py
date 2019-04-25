#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ud_class import Model
from vocabulary import cefr_dictionary, phrasal_list_big
from grammar_properties import get_non_verb_phrase_properties, get_verb_phrase_properties 
from collections import OrderedDict
import copy
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import nltk
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))
from string import punctuation
full_punctuation = punctuation + "–" + "," + "»" + "«" + "…" +'’'

import argparse
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('file', help='path to the file with raw text')
args = parser.parse_args()

DEBUG = args.debug
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

def lemmatize_from_udmap(conllu_map):
    sentences_list = []
    for sentence in conllu_map:
        line = ''
        for word in sentence: 
            line += word[2] + ' '
        sentences_list.append(line.strip())
        #print()
    return sentences_list

def get_tf_idf_dict(lemm_text_list, save_to_csv = False):
    vect = TfidfVectorizer(stop_words = stopWords)
    tfidf_matrix = vect.fit_transform(lemm_text_list)
    df = pd.DataFrame(tfidf_matrix.toarray(), columns = vect.get_feature_names())
    #print(df.head())
    if (save_to_csv): df.to_csv("./text_0_tfidf.xlsx", sep = '\t')
    tf_idf_dict = df.to_dict()
    return tf_idf_dict

def create_map(conllu_map, tf_idf_dict):
    text_map = []
    sentence_ind = 0
    for sentence in conllu_map:
        sentence_map = []
        real_index = 1
        for word in sentence: 
            weight = OrderedDict([("word", word[1]),("lemma",word[2]), ("vocabulary_prop",(OrderedDict([("vocab_importane", 0),("nominal_index",word[0])])))])
            
            lemma_lower = word[2].lower()
            if (lemma_lower in tf_idf_dict):
                weight['vocabulary_prop']["vocab_importane"] = tf_idf_dict[lemma_lower][sentence_ind]
            sentence_map.append(weight)
        text_map.append(sentence_map)
        sentence_ind += 1
    return text_map

def vocabulary_analysis(text_map_input, levels_dictionaries, debug = False):
    text_map = copy.deepcopy(text_map_input)
    level_collected_vocab = OrderedDict([('A1',[]),('A2',[]),('B1',[]), ('B2',[]), ('C',[]),('undefined_level',[])])
    level_collected_weight = OrderedDict([('A1',0),('A2',0),('B1',0),('B2',0),('C',0)])
    level_list = ['A1','A2','B1','B2','C']

    for sentence in text_map[0]:
        for word in sentence:
            low_lemma = word['lemma'].lower()
            low_lemma_clean = ''
            for char in low_lemma:
                if char not in full_punctuation:
                    low_lemma_clean += char
            
            found_in_dict = False
            for level in level_list:
                #print("level on air", level)
                if 'phrasal_verb' in word['vocabulary_prop']:
                    word['vocabulary_prop']['level'] = 'B1'
                    break
                if(low_lemma_clean in levels_dictionaries[level]):
                    #print("WORD FOUND",low_lemma_clean,  level)
                    level_collected_vocab[level].append((low_lemma_clean,word['vocabulary_prop']['vocab_importane']))
                    level_collected_weight[level] += word['vocabulary_prop']['vocab_importane']
                    word['vocabulary_prop']['level'] = level
                    found_in_dict = True
                    break
            if not found_in_dict:
                level_collected_vocab['undefined_level'].append((low_lemma_clean,word['vocabulary_prop']['vocab_importane']))
    total_identified_weights = 0
    for key, val in  level_collected_weight.items():
        total_identified_weights += val

    for key, val in  level_collected_weight.items():
        if(total_identified_weights > 0):
            level_collected_weight[key] = round(level_collected_weight[key]/total_identified_weights,2)

    return text_map, level_collected_vocab, level_collected_weight

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
                    """
                    if( potential_phrasal_verb in  phrasal_list_EASY):
                        #print("EASY PV DETECTED")
                        if abs(int(first_index) - int(second_index)) > 2:
                            vocab_properties_log[first_index] = "dist_easy_phrasal_verb"
                            vocab_properties_log[second_index] = "dist_easy_phrasal_verb"
                        else:
                            vocab_properties_log[first_index] = "easy_phrasal_verb"
                            vocab_properties_log[second_index] = "easy_phrasal_verb"
                    """
                    if(potential_phrasal_verb in phrasal_list_big):
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
        


def calculate_grammar(text_map):
    level_list = ['A1','A2','B1','B2','C']
    a1_gramm = {'PresSimp','PresCont','there_is_are'}
    a2_gramm = {'PastCont','modal_have_to','ZeroCond','FirstCond','Gerund','PrPerf','FutSimp'}
    b1_gramm = {'FutCont','PastPerf','PrPerfCont','SecondCond','ThirdCond','PresSimp_Passive', 'PastSimp_Passive','FutSimp_Passive'}
    b2_gramm = {'FutPerfCont', 'FutPerf','PastPerfCont'}
    c_gramm = {'PastPerf_Passive','PrPerf_Passive','FutPerf_Passive','PresCont_Passive','PastCont_Passive'}
    level_gramm = OrderedDict([('A1',a1_gramm),('A2',a2_gramm),('B1',b1_gramm), ('B2',b2_gramm), ('C',c_gramm)])
    level_collected_gramm = OrderedDict([('A1',[]),('A2',[]),('B1',[]), ('B2',[]), ('C',[])])
    level_grammar_collected_weight = OrderedDict([('A1',0),('A2',0),('B1',0),('B2',0),('C',0)])

    for sentence in text_map[0]:
        for word in sentence:
            if 'grammar_prop' in word:
                #print("GRAMMAR FOUND", word['grammar_prop'])
                for level in level_list:
                    if word['grammar_prop'] in level_gramm[level]:
                        level_collected_gramm[level].append((word['lemma'], word['grammar_prop']))
                        level_grammar_collected_weight[level] += 1
    total_identified_weights = 0
    for key, val in  level_grammar_collected_weight.items():
        total_identified_weights += val

    for key, val in  level_grammar_collected_weight.items():
        if(total_identified_weights > 0 ):
            level_grammar_collected_weight[key] = round(level_grammar_collected_weight[key]/total_identified_weights,2)

    return level_collected_gramm,level_grammar_collected_weight

def get_map(text_line,model):
    conllu = get_conllu(text_line, model, print_output = DEBUG)
    conllu_text_map = get_conllu_text_map(conllu)
    #print(conllu_text_map)
    lemm_sentences = lemmatize_from_udmap(conllu_text_map)
    tf_idf_dict = get_tf_idf_dict (lemm_sentences)
    text_map = create_map(conllu_text_map, tf_idf_dict)
    text_analysis_map = grammar_analysis(conllu_text_map, text_map)

    text_map_voc, level_collected_vocab, level_collected_weight = vocabulary_analysis(text_analysis_map, cefr_dictionary)
    level_collected_gramm, level_grammar_collected_weight = calculate_grammar(text_analysis_map)
    

    return text_analysis_map, level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight

def calculate_level(vocab_dict, vocab_weights_dict, grammar_dict, grammar_count_dict):
    print("====VOCABULARY LISTS===")
    for key, values_list in vocab_dict.items():
        print("======",key,"=======")
        for val in values_list:
            print(val)
    print('\n\n')
    print("====VOCABULARY WEIGHTS===")
    for key, values_list in vocab_weights_dict.items():
        print("======",key,"=======")
        print(values_list)
    print('\n\n')
    print("====GRAMMAR LIST===")
    for key, values_list in grammar_dict.items():
        print("======",key,"=======")
        print("total occurencies", len(values_list))
        for val in values_list:
            print(val)
    print('\n\n')
    print("====GRAMMAR PERCENTAGE===")
    for key, values_list in grammar_count_dict.items():
        print("======",key,"=======")
        print(values_list)

text = ''
with open(args.file, "r", encoding = "utf-8") as text_file:
    for line in text_file.readlines():
        text += line + ' '
text_analysis_map, level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight = get_map(text, model)

for sentence in text_analysis_map[0]:
    for word in sentence:
        print(word,'\n')
    print("====================")
print('\n\n')

calculate_level(level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight)
