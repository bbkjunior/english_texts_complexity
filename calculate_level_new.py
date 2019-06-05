#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ud_class import Model
from vocabulary import cefr_dictionary, phrasal_list_big
from grammar_properties import get_non_verb_phrase_properties, get_verb_phrase_properties 

from collections import OrderedDict
import copy
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import nltk
#from nltk.corpus import stopwords
#stopWords = set(stopwords.words('english'))
from string import punctuation
full_punctuation = punctuation + "–" + "," + "»" + "«" + "…" +'’'
import operator
import re
#import nltk
#nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer 



DEBUG = False

model = Model('./UDPIPE/english-ud-2.0-170801.udpipe')

def get_conllu(text_line, model, print_output = DEBUG):
    """получаем разобранный текст"""
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
    """извлекаем только нуную инвормацию (без пунктуации)"""
    conllu_text_map = []
    conllu_sentence_map = []
    for line in conllu_parsed_object.split('\n'):
        if line :
            if line[0].isdigit():
                split_items = line.split('\t')
                if split_items[3] != "PUNCT":
                    conllu_sentence_map.append(split_items)
            else:
                if(len(conllu_sentence_map) > 0):
                    conllu_text_map.append(conllu_sentence_map)
                    conllu_sentence_map = []   
    if(len(conllu_sentence_map) > 0):
        conllu_text_map.append(conllu_sentence_map)
    return conllu_text_map

def lemmatize_from_udmap(conllu_map):
    """лемматизируем текст из результатов работы udpipe"""
    sentences_list = []
    for sentence in conllu_map:
        line = ''
        for word in sentence: 
            line += word[2] + ' '
        sentences_list.append(line.strip())
    return sentences_list

def get_tf_idf_dict(lemm_text_list, save_to_csv = False):
    """считаем tf-idf, экспортируем словарь со значениями"""
    vect = TfidfVectorizer(stop_words = "english")
    if len(lemm_text_list) == 0:
        return None
    tfidf_matrix = vect.fit_transform(lemm_text_list)
    df = pd.DataFrame(tfidf_matrix.toarray(), columns = vect.get_feature_names())
    #print(df.head())
    if (save_to_csv): df.to_csv("./text_0_tfidf.xlsx", sep = '\t')
    tf_idf_dict = df.to_dict()
    return tf_idf_dict

def create_map(conllu_map, tf_idf_dict):
    """создаем карту текста (лист из списка свойств слов в формате json"""
    text_map = []
    sentence_ind = 0
    for sentence in conllu_map:
        sentence_map = []
        real_index = 1
        for word in sentence: 
            weight = OrderedDict([("word", word[1]),("lemma",word[2]), ("vocabulary_prop",(OrderedDict([("vocab_importane", 0),("nominal_index",word[0])])))])
            
            lemma_lower = word[2].lower()
            if (lemma_lower in tf_idf_dict):
                weight['vocabulary_prop']["vocab_importane"] = round(tf_idf_dict[lemma_lower][sentence_ind] * 10,0)#для того чтобы была эквивалентность количеству условных единиц слова
            sentence_map.append(weight)
        text_map.append(sentence_map)
        sentence_ind += 1
    return text_map


def build_subtree_branch(head_word_nominal_index, pos_word_dict,verb_phrases_dict, word_leave):
    """функция для заполнения синтаксического поддерева"""
    if (int(head_word_nominal_index)!= 0):
        current_head_word = pos_word_dict[head_word_nominal_index][0]
        current_head_pos = pos_word_dict[head_word_nominal_index][1][1]
        if(current_head_word in verb_phrases_dict):
            verb_phrases_dict[current_head_word].append(word_leave)
        else:
            verb_phrases_dict[current_head_word] = []
            verb_phrases_dict[current_head_word].append(word_leave)     


def grammar_analysis(conllu_map,text_map_input, show_trees = DEBUG, show_log = DEBUG):
    """собираем грамматическую информацию и инфу о фразовых глаголах"""
    assert len(conllu_map) == len(text_map_input) #sentences count is equal
    text_map = copy.deepcopy(text_map_input)
    
    for sentence_conllu, text_map_sentence in zip(conllu_map,text_map):
        pos_word_dict = {}#СОБИРАЕМ СПИСОК СВАОЙСТВ ВСЕХ СЛОВ ПРЕДЛОЖЕНИЯ ДЛЯ ПОСЛЕДУЮЩЕГО ОБРАЩЕНИЯ
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
            if (int(word_leave[6]) != 0):
                if word_leave[6] in pos_word_dict:
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
def vocabulary_analysis(text_map_input, levels_dictionaries, debug = False):
    """собираем список слов по уровням"""
    lemmatizer = WordNetLemmatizer()
    text_map = copy.deepcopy(text_map_input)
    level_collected_vocab = OrderedDict([('A1',[]),('A2',[]),('B1',[]), ('B2',[]), ('C',[]),('undefined_level',[])])
    level_collected_weight = OrderedDict([('A1',0),('A2',0),('B1',0),('B2',0),('C',0)])
    level_list = ['A1','A2','B1','B2','C']
    #unique_words = [] Вопрос обсуждаемый - брать все слова или только уникальные
    for sentence in text_map[0]:
        for word in sentence:
            low_lemma = word['lemma'].lower()
            low_lemma_clean = ''
            for char in low_lemma:
                if char not in full_punctuation:
                    low_lemma_clean += char
            #if low_lemma_clean not in unique_words:
            #unique_words.append(low_lemma_clean)
            found_in_dict = False
            for level in level_list:
                if 'phrasal_verb' in word['vocabulary_prop']:
                    word['vocabulary_prop']['level'] = 'B1'
                    break
                if(low_lemma_clean in levels_dictionaries[level]):
                    level_collected_vocab[level].append((low_lemma_clean,word['vocabulary_prop']['vocab_importane']))
                    level_collected_weight[level] += word['vocabulary_prop']['vocab_importane']
                    word['vocabulary_prop']['level'] = level
                    found_in_dict = True
                    break                    
            if not found_in_dict:
                add_lemma = lemmatizer.lemmatize(low_lemma_clean)
                for level in level_list:
                    if(add_lemma in levels_dictionaries[level]):
                        level_collected_vocab[level].append((low_lemma_clean,word['vocabulary_prop']['vocab_importane']))
                        level_collected_weight[level] += word['vocabulary_prop']['vocab_importane']
                        word['vocabulary_prop']['level'] = level
                        found_in_dict = True
                        break
            if not found_in_dict and not re.search('[0-9]', low_lemma_clean):
                level_collected_vocab['C'].append((low_lemma_clean,word['vocabulary_prop']['vocab_importane']))
                level_collected_vocab['undefined_level'].append((low_lemma_clean,word['vocabulary_prop']['vocab_importane']))
    total_identified_weights = 0
    for key, val in  level_collected_weight.items():
        total_identified_weights += val

    for key, val in  level_collected_weight.items():
        if(total_identified_weights > 0):
            level_collected_weight[key] = round(level_collected_weight[key]/total_identified_weights,4)

    return text_map, level_collected_vocab, level_collected_weight        


def calculate_grammar(text_map):
    """анализируем реально присутствующую в тексте грамматику"""
    level_list = ['A1','A2','B1','B2','C']
    a1_gramm = {'PresSimp','PresCont','there_is_are'}
    a2_gramm = {'PastCont','modal_have_to','ZeroCond','Gerund','FutSimp','PastSimp'}
    b1_gramm = {'FutCont','FirstCond','PresSimp_Passive', 'PastSimp_Passive','FutSimp_Passive','PrPerf'}
    b2_gramm = {'FutPerfCont', 'FutPerf','SecondCond','PrPerfCont'}
    c_gramm = {'PastPerf_Passive','PrPerf_Passive','FutPerf_Passive','PresCont_Passive','PastCont_Passive','ThirdCond','PastPerfCont','PastPerf'}
    level_gramm = OrderedDict([('A1',a1_gramm),('A2',a2_gramm),('B1',b1_gramm), ('B2',b2_gramm), ('C',c_gramm)])
    level_collected_gramm = OrderedDict([('A1',[]),('A2',[]),('B1',[]), ('B2',[]), ('C',[])])
    level_grammar_collected_weight = OrderedDict([('A1',0),('A2',0),('B1',0),('B2',0),('C',0)])

    for sentence in text_map[0]:
        for word in sentence:
            if 'grammar_prop' in word:
                for level in level_list:
                    if word['grammar_prop'] in level_gramm[level]:
                        level_collected_gramm[level].append((word['lemma'], word['grammar_prop']))
                        level_grammar_collected_weight[level] += 1
    total_identified_weights = 0
    for key, val in  level_grammar_collected_weight.items():
        total_identified_weights += val

    for key, val in  level_grammar_collected_weight.items():
        if(total_identified_weights > 0 ):
            level_grammar_collected_weight[key] = round(level_grammar_collected_weight[key]/total_identified_weights,4)

    return level_collected_gramm,level_grammar_collected_weight

def get_map(text_line,model):
    conllu = get_conllu(text_line, model, print_output = DEBUG)
    conllu_text_map = get_conllu_text_map(conllu)
    lemm_sentences = lemmatize_from_udmap(conllu_text_map)
    if not lemm_sentences:
        return None, None,  None, None, None
    tf_idf_dict = get_tf_idf_dict (lemm_sentences)
    if not tf_idf_dict:
        return None, None,  None, None, None
    text_map = create_map(conllu_text_map, tf_idf_dict)
    text_analysis_map = grammar_analysis(conllu_text_map, text_map)
    text_map_voc, level_collected_vocab, level_collected_weight = vocabulary_analysis(text_analysis_map, cefr_dictionary)
    level_collected_gramm, level_grammar_collected_weight = calculate_grammar(text_map_voc)
    return text_map_voc, level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight

def get_features(vocab_dict, vocab_weights_dict, grammar_dict, grammar_count_dict):
    all_features = []
    vocab_dict_feat = OrderedDict([('A1',0),('A2',0),('B1',0),('B2',0),('C',0)])
    #vocab_features
    #print(vocab_dict)
    vocab_imp_sum = 0
    for key, values_list in vocab_dict.items():
        if key != "undefined_level":
            for val in values_list:
                vocab_dict_feat[key] += int(val[1])
                vocab_imp_sum += int(val[1])
    if(vocab_imp_sum > 0):
        for key, values_list in vocab_dict_feat.items():
            vocab_dict_feat[key] /= vocab_imp_sum
    #print(vocab_dict_feat)
    all_features.extend(list(vocab_dict_feat.values()))

    #grammar_features
    gramm_indexes_dict = {'PresSimp':0,'PresCont':1,'there_is_are':2, 'PastCont':3,'modal_have_to':4,'ZeroCond':5,'Gerund':6,'FutSimp':7,'PastSimp':8, 'FutCont':9,'FirstCond':10,'PresSimp_Passive':11, 'PastSimp_Passive':12,'FutSimp_Passive':13,'PrPerf':14,'FutPerfCont':15, 'FutPerf':16,'SecondCond':17,'PastPerf':18,'PrPerfCont':19,'PastPerf_Passive':20,'PrPerf_Passive':21,'FutPerf_Passive':22,'PresCont_Passive':23,'PastCont_Passive':24,'ThirdCond':25,'PastPerfCont':26}
    gramm_features_list = [0] * 27
    gramm_features_list_sum = 0
    for key, values_list in grammar_dict.items():
        for val in values_list:
            gramm_features_list[gramm_indexes_dict[val[1]]] += 1
            gramm_features_list_sum += 1
    if(gramm_features_list_sum > 0):
        gramm_features_list = [elt / gramm_features_list_sum for elt in gramm_features_list] 
    all_features.extend(gramm_features_list)
    #print(gramm_features_list)
    #print(all_features)
    return all_features



def calculate_level(vocab_dict, vocab_weights_dict, grammar_dict, grammar_count_dict, show_output = False):
    """подсчитываем финальные показатели. Грамматике дается вес 0.3 лексике - 0.7"""
    if show_output:
        print("====VOCABULARY LISTS===")
        for key, values_list in vocab_dict.items():
            print("======",key,"=======")
            for val in values_list:
                print(val)
     #percentile method   
    key_level_value_dict =  {'A1':20, 'A2':40,'B1':65,'B2':90,'C':105}
    vocab_complexity_list = []
    for key, values_list in vocab_dict.items():
        if key != "undefined_level":
            for val in values_list:
                one_element_list = [key_level_value_dict[key]] * int(val[1])
                vocab_complexity_list.extend(one_element_list)
    if len (vocab_complexity_list) > 0:           
        vocab_complexity = np.percentile(vocab_complexity_list, 75)#!!!!75>55
    else:
        return "Text seems to be empty"
    if show_output:
        print('\n\n')
        print("====VOCABULARY WEIGHTS===")
        for key, level_vocab_weight in vocab_weights_dict.items():
            if show_output: 
                print("======",key,"=======")
                print(level_vocab_weight)

    if show_output:
        print('\n\n')
        print("====GRAMMAR LIST===")
        for key, values_list in grammar_dict.items():
            print("======",key,"=======")
            print("total occurencies", len(values_list))
            for val in values_list:
                print(val)

        print('\n\n')
        print("====GRAMMAR WEIGHTS===")
    for key, level_grammar_weight in grammar_count_dict.items():
        if show_output:
            print("======",key,"=======")
            print(level_grammar_weight)

        grammar_complexity_list = []    
    grammar_adjusting_dict = OrderedDict([('A1',1),('A2',2),('B1',4),('B2',6),('C',8)])
    #percentile method  
    for key, values_list in grammar_dict.items():
            for val in values_list:
                one_element_list = [key_level_value_dict[key]] * int(grammar_adjusting_dict[key])
                #print("one_element_list",one_element_list) 
                grammar_complexity_list.extend(one_element_list)
    if (len(grammar_complexity_list)):
        grammar_complexity = np.percentile(grammar_complexity_list, 75)
    else:
        grammar_complexity = 0
    overal_complexity = 0.6 * vocab_complexity + 0.4 * grammar_complexity
    if (overal_complexity == 0):
        return "Text seems to be empty"

    if show_output:
        #print("vocab_complexity_list",vocab_complexity_list )
        print("vocab_complexity 75 percentile",vocab_complexity ) 
        #print("grammar_complexity_list",grammar_complexity_list)
        print("Grammar_complexity 75 percentile",grammar_complexity )
        print("NEW TYPE COMPLEXITY", overal_complexity)

    find_distance_dict = OrderedDict([('A1',0),('A2',0),('B1',0),('B2',0),('C',0)])
    adjusted_borders_dict =  {'A1':30, 'A2':40,'B1':60,'B2':70,'C':90}
    for key, value in key_level_value_dict.items():
        #find_distance_dict[key] = abs(key_level_value_dict[key] - overal_complexity) 
        find_distance_dict[key] = abs(adjusted_borders_dict[key] - overal_complexity) 
    
    sorted_final_calculation = sorted(find_distance_dict.items(), key=operator.itemgetter(1))
    if show_output:
        print('\n\n')
        print("====OVERALL CALCULATION===")
        for lvl in sorted_final_calculation:
            print(lvl)
    cefr2lev = {'A1':"Beginner", 'A2': "Elementary/Pre-Intermediate",'B1':"Intermediate",'B2':"Upper-Intermediate",'C':"Advanced"}
    level_repsone = {'level': cefr2lev[sorted_final_calculation[0][0]]}
    return level_repsone

def get_level_from_raw_text(text):
    try:
        text_analysis_map, level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight = get_map(text, model)
        if not text_analysis_map:
            return "Text seems to be empty"
        level = calculate_level(level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight)
        level_val = level['level']
        return level_val 
    except:
        return "Level calculation failed"
def get_features_from_raw_text(text):
    text_analysis_map, level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight = get_map(text, model)
    text_features = get_features(level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight)
    return text_features







