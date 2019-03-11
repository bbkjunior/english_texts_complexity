import argparse
import os

import pandas as pd
import string
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import wordnet
import nltk

import spacy
nlp = spacy.load('en')

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import numpy as np
from scipy.sparse.csr import csr_matrix

from sklearn.feature_extraction.text import TfidfTransformer

parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-d', '--print_debug_message', help='print out calculation process', action="store_true")
parser.add_argument('-w', '--show_calucated_weights', help='who weights of the whole text', action="store_true")
parser.add_argument('-s', '--show_difficult', help='show difficult words weights', action="store_true")
parser.add_argument('file', help='path to the file with raw text')
args = parser.parse_args()


#ЗАДАЕМ СЛОВАРЬ ДЛЯ РАЗВОРАЧИВАНИЯ СОКРАЩЕННЫХ ФРАЗ
contr = pd.read_csv("./materials/contractions.csv")
contractions = {}
for key, val in zip(contr['short'],contr['long']):
    contractions[key] = val

#ЗАДАЕМ БАЗОВЫЙ СЛОВАРЬ 
basic_vocabulary = []
with open("./materials/A1_vocab_processed.txt", "r") as voc:
    for word in voc.readlines():
        basic_vocabulary.append(word[:-1])

adjectives = []
with open("./materials/common_adj.txt", "r") as common_adj:
    for word in common_adj.readlines():
        adjectives.append(word[:-1])
        
common_uncountable = []
with open("./materials/common_unountable_manually_filtered.txt", "r") as common_unctbl:
    for word in common_unctbl.readlines():
        common_uncountable.append(word[:-1])

countries = []
with open("./materials/countries.txt", "r") as cntr:
    for word in cntr.readlines():
        countries.append(word[:-1])

names = []
with open("./materials/names.txt", "r") as names_file:
    for word in names_file.readlines():
        names.append(word[:-1])
        
#print(len(basic_vocabulary), len(adjectives), len(common_uncountable), len(countries), len(countries), len(names))
final_basic_vocabulary = basic_vocabulary
final_basic_vocabulary.extend(adjectives)
final_basic_vocabulary.extend(common_uncountable)
final_basic_vocabulary.extend(countries)
final_basic_vocabulary.extend(names)

#ЗАДАЕМ СЛОВАРЬ ФРАЗОВЫХ ГЛАГОЛОВ
phrasal_list = []
with open("./materials/phrasal_verbs.txt", "r") as pv_doc:
    for pv in pv_doc:
        phrasal_list.append(pv[:-1])
        
#РАЗБИВАЕМ НА ПРЕДЛОЖЕНИЯ, ЧИСТИМ ПУНКТУАЦИЮ, ПРИВОДИМ К НИЖНЕМУ РЕГИСТРУ       
puncuation_primary = string.punctuation + "’" +"“" + "”" + "…" + "'"
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
lemmatizer = WordNetLemmatizer()
def punct_setnence_lower (line, sent_detector, debug = False, deep_debug = False):
    initial_sentences_list = sent_detector.tokenize(line.strip())
    final_sentences_list = []
    
    for sentence in initial_sentences_list:
        if(debug): print("sentence:", sentence)
        cleaned_line = ''
        #clean by word
        for word in sentence.split():
            if(debug): print(word)
            clean_word =''
            for char in word:
                if(deep_debug): print("char before cleaning:", char)
                if char not in puncuation_primary and char.isalpha():
                    clean_word += char.lower()
                    if(deep_debug): print("char after cleaning:", char.lower())
                else:
                    clean_word += ' '
                    if(deep_debug): print("char has been deleted")
            clean_word = clean_word.lstrip()
            if(debug):print("non punctuation and lower:",clean_word)       

            if (clean_word in contractions):
                if(debug):print("word before contractions parsing:",clean_word)
                clean_word = ''.join(contractions[clean_word])
                if(debug):print("word after contractions parsing:",clean_word)
            if(debug): print("finally cleaned word/s:",clean_word)    
            cleaned_line += clean_word + ' '
        
        """
        #handle abbreviations delete dots only in the end    
        for char_ind in range(len(cleaned_line) - 3, len(cleaned_line)):
            max_dot_index = len(cleaned_line)
            if cleaned_line[char_ind] == ".":
                if(char_ind < max_dot_index): max_dot_index = char_ind
                break
        cleaned_line = cleaned_line[:max_dot_index]   """ 
        cleaned_line = re.sub(' +', ' ', cleaned_line)
        cleaned_line = cleaned_line.rstrip()
        cleaned_line = cleaned_line.lstrip()
        final_sentences_list.append(cleaned_line)
    return final_sentences_list
    
#ЗАДАЕМ ФУНКЦИЮ ДЛЯ ПОЛУЧЕНИЯ ГРАММАТИЧЕСКОЙ КАРТЫ ТЕКСТА
def get_sent_gramm_features_map(text):
    text_grammar_map = []
    for sentence in text:
        split_sent_list = sentence.split()
        grammar_map = [None] * len(split_sent_list)  
        parsed_sentence =  nlp(sentence)   
        #print(len(parsed_sentence), len(grammar_map))
        if(len(parsed_sentence) != len(split_sent_list)):
            print("ASSERTION ERROR!")
            print("parsed_sentence", len(parsed_sentence), "split_sent_list", len(split_sent_list),len(grammar_map))
            print( "split_sent_list", split_sent_list)
            for element_ind in range(len(parsed_sentence)):
                print("parsed lemma:", parsed_sentence[element_ind].lemma_, element_ind)
        assert (len(parsed_sentence) == len(grammar_map))
        for gramm_ind in range(len(split_sent_list)):
            #print(parsed_sentence[gramm_ind])
            if(parsed_sentence[gramm_ind].lemma_[0] == "-"):
                parsed_sentence[gramm_ind].lemma_ = parsed_sentence[gramm_ind].text
            grammar_map[gramm_ind] = (parsed_sentence[gramm_ind].lemma_, nlp.vocab.morphology.tag_map[parsed_sentence[gramm_ind].tag_])
        text_grammar_map.append(grammar_map)
    return text_grammar_map
    
#ЛЕММАТИЗИРУЕМ ТЕКСТ
def get_lemm_text(text_gramm_map):
    lemm_text = []
    for sentence in text_gramm_map:
        sentence_lemm = ''
        for word in sentence:
            sentence_lemm += word[0] + ' '
        sentence_lemm = sentence_lemm[:-1]
        lemm_text.append(sentence_lemm)
        
    return lemm_text

#ВЫЧИСЛЯЕМ ТФИДФ    
def get_tf_idf_dict(lemm_text_list, save_to_csv = False):
    vect = TfidfVectorizer(stop_words = 'english')
    tfidf_matrix = vect.fit_transform(lemm_text_list)
    df = pd.DataFrame(tfidf_matrix.toarray(), columns = vect.get_feature_names())
    #print(df.head())
    if (save_to_csv): df.to_csv("./text_0_tfidf.xlsx", sep = '\t')
    tf_idf_dict = df.to_dict()
    return tf_idf_dict

#ЗАДАЕМ СПИСОК ВЕСОВ СЛОВ ДЛЯ ПОСЛЕДУЮЩЕГО ЗАПОЛНЕНИЯ ФИЧАМИ    
def get_weights_empty_list(gramm_map_text):
    weights_list = []
    for sentence in gramm_map_text:
        #print(sentence)
        sentence_weights = []
        for element in sentence:
            weight = {"word" : element[0], "weight": 0}
            sentence_weights.append(weight)
        weights_list.append(sentence_weights)
    return weights_list

#ЗАДАЕМ ФУНКЦИЮ ДЛЯ ВЫЯВЛЕНИЯ СОЖНОЙ ГРАММАТИКИ 
def get_difficult_grammar(text_grammar_map, weights_list, debug = False):
    for sentence_grammar_map, sentence_weights in zip(text_grammar_map,weights_list):
        for el_ind in range(len(sentence_grammar_map)):
            #print(sentence_grammar_map[el_ind])
            
            if('Aspect' in sentence_grammar_map[el_ind][1]):
                #present perfect
                if ( sentence_grammar_map[el_ind][1]['Aspect'] == 'perf' ):
                    if(sentence_grammar_map[el_ind - 2][0] == 'have' or sentence_grammar_map[el_ind - 1][0] == 'have'):
                        if(debug): print("PRESENT PERFECT")
                        if(debug): print(sentence_grammar_map[el_ind - 1])
                        if(debug): print(sentence_grammar_map[el_ind])

                        sentence_weights[el_ind]["diff_grammar"] = "pr_perf"
                        sentence_weights[el_ind - 1]["diff_grammar"] = "pr_perf"
                
                
                elif(sentence_grammar_map[el_ind][1]['Aspect'] == 'prog'):
                    #future continious check "will + be + v-ing"
                    if (sentence_grammar_map[el_ind - 1][0] == 'be' and sentence_grammar_map[el_ind - 2][0] == 'will'):
                        if(debug): print("FUTURE CONTINIOUS")                       
                        if(debug): print("prev word is", sentence_grammar_map[el_ind - 2])
                        if(debug): print("prev word is", sentence_grammar_map[el_ind - 1])
                        if(debug): print(sentence_grammar_map[el_ind])
                        sentence_weights[el_ind]["diff_grammar"] = "fut_cont"
                        sentence_weights[el_ind - 1]["diff_grammar"] = "fut_cont"
                        sentence_weights[el_ind - 2]["diff_grammar"] = "fut_cont"
                   #past continious was/were + v-ing"     
                    elif (sentence_grammar_map[el_ind - 1][0] == 'be' and 'Tense' in sentence_grammar_map[el_ind -1][1]):
                        if(sentence_grammar_map[el_ind -1][1]['Tense'] == 'past'):
                            if(debug): print("PAST CONTINIOUS")
                            if(debug): print(sentence_grammar_map[el_ind])
                            if(debug): print("prev word is", sentence_grammar_map[el_ind - 1])
                            sentence_weights[el_ind]["diff_grammar"] = "past_cont"
                            sentence_weights[el_ind - 1]["diff_grammar"] = "past_cont"
                        
                
    return weights_list

#ЗАДАЕМ ФНУКЦИЮ ДЛЯ ПОИСКА ФРАЗОВЫХ ГЛАГОЛОВ    
def get_phrasal_verbs(text_grammar_map, weights_list, debug = False):
    for sentence_grammar_map, sentence_weights in zip(text_grammar_map,weights_list):
        for el_ind in range(1, len(sentence_grammar_map)):  
            for searh_ind in range(1, 3):
                try_phrase = sentence_grammar_map[el_ind - searh_ind][0] + ' ' + sentence_grammar_map[el_ind][0]
                #print(try_phrase)
                if(try_phrase in phrasal_list):
                    if(debug): print("Phrasal Verb found:", try_phrase)
                    sentence_weights[el_ind]["phrasal_verb"] = "yes"
                    sentence_weights[el_ind - searh_ind]["phrasal_verb"] = "yes"
    return weights_list
    
#ПРИСВАИВАЕМ ВЕСА ТФИДФ 
def assign_tf_idf(text_grammar_map, weights_list, tf_idf_dict):
    assert (len(text_grammar_map) == len(weights_list))
    for sentence_ind in range(len(text_grammar_map)):
        for el_ind in range(len(text_grammar_map[sentence_ind])):
            lemma = weights_list[sentence_ind][el_ind]["word"]
            
            if (lemma in tf_idf_dict):
                weights_list[sentence_ind][el_ind]["weight"] = tf_idf_dict[lemma][sentence_ind]
                #print(lemma, tf_idf_dict[lemma][sentence_ind])
            else:
                weights_list[sentence_ind][el_ind]["weight"] = 0.05
                #print(lemma, "not found")
                
    return weights_list
    
    
#ДЕЛИМ НА СЛОЖНЫЕ И НЕ СЛОЖНЫЕ В СООТВЕТСВИИ С ПОЛУЧЕННЫМИ ФИЧАМИ
def split_into_groups(text_weights, show_difficult = False):
    difficult_vocabulary = []
    easy_vocabulary = []
    for sentence_weights in text_weights:
        for word_weight in sentence_weights:
            #print(word_weight)
            if('diff_grammar' in word_weight or 'phrasal_verb' in word_weight or word_weight['word'] not in basic_vocabulary):
                difficult_vocabulary.append(word_weight)
            else:
                easy_vocabulary.append(word_weight)
    if(show_difficult):
        print("DIFFICULT WORDS IN THIS TEXT ARE")
        for element in difficult_vocabulary:
            print(element)
    return easy_vocabulary, difficult_vocabulary
    
def calculate_level(easy_words_weights, difficults_words_weights, debug = False):
    tf_idf_easy = 0
    for easy_w_w in easy_words_weights:
        tf_idf_easy += easy_w_w['weight']
        
    tf_idf_diff = 0
    for diff_w_w in difficults_words_weights:
        tf_idf_diff += diff_w_w['weight']
        
    if(debug):print("easy words:", len(easy_words_weights), "difficult words:", len(difficults_words_weights))
    if(debug):print("easy tfidf sum:",tf_idf_easy, "difficult tfidf sum:",tf_idf_diff)
    overall_weights = tf_idf_easy + tf_idf_diff
    if(debug):print("relative tfidf", round(tf_idf_easy/overall_weights, 2), round(tf_idf_diff/overall_weights, 2))
    if(round(tf_idf_diff/overall_weights, 2) >= 0.3):
        print("text is very diffcult, diff relative weight is more then 0.3")
    if(round(tf_idf_diff/overall_weights, 2) > 0.2 and round(tf_idf_diff/overall_weights, 2) < 0.3):
        print("text is moderate")
    if(round(tf_idf_diff/overall_weights, 2) <= 0.2):
        print("text is quite easy")

        
def calculate_text_level(raw_text, print_debug_message = False, show_calucated_weights = False, show_difficult_words_weights = False):
    processed_text = punct_setnence_lower(raw_text,sent_detector)
    
    grammar_map = get_sent_gramm_features_map(processed_text)
    
    text_lemm = get_lemm_text(grammar_map)
    
    tfidf_dict = get_tf_idf_dict(text_lemm)
    
    weights = get_weights_empty_list(grammar_map)
    
    weights = get_difficult_grammar(grammar_map,weights, debug = print_debug_message)
    weights = get_phrasal_verbs(grammar_map,weights, debug = print_debug_message)
    weights = assign_tf_idf(grammar_map, weights, tfidf_dict)
    
    if(show_calucated_weights): 
        print("WEIGHTS HAVE BEEN CALCULATED AS FOLLOWS (sentence by sentence)")
        for sent_weights in weights:
            for word_weight in sent_weights:
                print(word_weight)
            print("\n")
    easy, difficult = split_into_groups(weights, show_difficult = show_difficult_words_weights)
    
    calculate_level(easy, difficult,  debug = print_debug_message)

text = ''
with open(args.file, "r", encoding = "utf-8") as text_file:
    for line in text_file.readlines():
        text += line + ' '
        
calculate_text_level(text, print_debug_message = args.print_debug_message, show_calucated_weights = args.show_calucated_weights, show_difficult_words_weights = args.show_difficult)