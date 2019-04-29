#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
from grammar_analysis_debug import get_map
from ud_class import Model
import argparse

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-p', '--print_positive_results', action='store_true')
parser.add_argument('-e', '--show_known_errors', action='store_true')
args = parser.parse_args()

PRINT_POSITIVE = args.print_positive_results

model = Model('./UDPIPE/english-ud-2.0-170801.udpipe')
def assert_analysis_results(real_grammar_log_input, real_vocab_log, ideal_gram_log, ideal_voc_log, sentence):
    real_grammar_log = copy.deepcopy(real_grammar_log_input)
    key_to_delete = []
    grmmar_inconsistence_detected = False
    vocab_inconsistence_detected = False
    already_printed_setnence = False
    for real_key, real_val in real_grammar_log.items():
        if not real_key.isdigit():
            key_to_delete.append(real_key)
    for key in key_to_delete:
        del real_grammar_log[key]
    #print("cleaned grammar prop dict",real_grammar_log )
    if len(list(real_grammar_log.values())) != len(list(ideal_gram_log.values())):
        if not PRINT_POSITIVE:
            print("Failed while checking <", sentence,">")
            print("||||GRAMMAR LOG ITMES QUANTITY IS NOT EQUAL||||")
            already_printed_setnence = True
    for real_key,real_item in real_grammar_log.items():
        if (real_key not in ideal_gram_log or real_grammar_log[real_key] != ideal_gram_log[real_key]):
            if not PRINT_POSITIVE and not already_printed_setnence:
                print("Failed while checking <", sentence,">")
                already_printed_setnence = True
                
            print(real_key, real_item, "||||IS NOT CORRECT GRAMMAR||||")
            grmmar_inconsistence_detected = True
    for ideal_key,ideal_val in ideal_gram_log.items():
        if (ideal_key not in real_grammar_log or real_grammar_log[ideal_key] != ideal_gram_log[ideal_key]):
            if not PRINT_POSITIVE and not already_printed_setnence:
                print("Failed while checking <", sentence,">")
                already_printed_setnence = True
            print(ideal_key, ideal_val, "||||IS MISSING FROM GRAMMAR ANALYSIS||||")
            grmmar_inconsistence_detected = True

    if len(list(real_vocab_log.values())) != len(list(ideal_voc_log.values())):
        print("||||VOCAB LOG ITMES QUANTITY IS NOT EQUAL||||")
    for real_key,real_item in real_vocab_log.items():
        if (real_key not in ideal_voc_log):
            if not PRINT_POSITIVE and not already_printed_setnence:
                print("Failed while checking <", sentence,">")
                already_printed_setnence = True
            print(real_key, real_item, "||||IS NOT CORRECT GRAMMAR||||")
            vocab_inconsistence_detected = True
    for ideal_key,ideal_val in ideal_voc_log.items():
        if (ideal_key not in real_vocab_log):
            if not PRINT_POSITIVE and not already_printed_setnence:
                print("Failed while checking <", sentence,">")
                already_printed_setnence = True
            print(ideal_key, ideal_val, "||||IS MISSING FROM GRAMMAR ANALYSIS||||")
            vocab_inconsistence_detected = True 
    if not grmmar_inconsistence_detected:
       if PRINT_POSITIVE: print("Gramamr OK (real log is)", real_grammar_log)
    else:
        print("||||GRAMMAR NOT CORRECT||||", real_grammar_log)
    if not vocab_inconsistence_detected:
       if PRINT_POSITIVE: print("Vocab OK (real log is)", real_vocab_log)
    else:
        print("||||VOCAB NOT CORRECT||||", real_vocab_log)
        
    if (already_printed_setnence):
        print()


def test():
    #CHECK WITH VERB AND WITH TO BE
    #Present Simple
    if PRINT_POSITIVE: print("==========CHECKING PRESENT SIMPLE==========")
    sentence = "I go to school"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'2': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "I do not go to school"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Do I go to school?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Does he go to school?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "HE DOESN'T GO TO this stupid SCHOOL?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "I am a pilot"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'2': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "He is a stupid doctor"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'2': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "They are here"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'2': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Are you there?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING PAST SIMPLE==========")
    sentence = "I went to school"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'2': 'PastSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "I didn't go to school"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PastSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    sentence = "Did I go to school"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PastSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "I were there"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'2': 'PastSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "My little freind was there"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PastSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Was my brother here?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'PastSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Were your brothers in this little country?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'PastSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING FUTURE SIMPLE==========")
    sentence = "I will go to school next summer"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'FutSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "They will really go to school next summer"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'FutSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Will they really go to school with us"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'FutSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "My friend will be there until eight o'clock"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'FutSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Will my dad be here"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'FutSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING PRESENT CONTINUOUS==========")
    sentence = "I am going there"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PresCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "My car is running out of fuel"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PresCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "They are trying to sort this out"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PresCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Are they going with you?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PresCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Is he trying to reveal the mystery with you?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PresCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING PAST CONTINUOUS==========")
    sentence = "I was going to the party"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PastCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "They were looking for you"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PastCont'}
    ideal_voc = {'3':"phrasal_verb", '4':"phrasal_verb"}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Were they trying to find you?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PastCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Was he going to the zoo that time?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PastCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING FUTURE CONTINUOUS==========")
    sentence = "My car will be working well the next Tuesday"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'5': 'FutCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Will he be getting ready for the homework?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'FutCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "I will be going throguht the arkness"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'FutCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING PRESENT PERFECT==========")
    sentence = "I have gone for a walk last night"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PrPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "I have been to Londong many-many years ago"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PrPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Have you ever been there?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PrPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "He hasn't been there for ages"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PrPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Has he gave up smoking"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PrPerf'}
    ideal_voc = {'3':'phrasal_verb','4':'phrasal_verb'}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING PAST PERFECT==========")
    sentence = "I had tried that food before"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PastPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "I had been in the cabinet with that person"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PastPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Had they already tried this food"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PastPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING FUTURE PERFECT==========")
    sentence = "I will have done that till eleven a.m"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'FutPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "I will have been to London until seven"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'FutPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Will these strong seamen have ever been to our river till next year?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'7': 'FutPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING PRESENT PERFECT CONTINUOUS==========")
    sentence = "I have been waiting for them for even hours"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PrPerfCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "He has been trying to figure this our"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PrPerfCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Has he been playing footbal more than three hours?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PrPerfCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING PAST PERFECT CONTINUOUS==========")
    sentence = "I had been waiting for them for even hours"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PastPerfCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Had I been waiting for them for even hours"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PastPerfCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========CHECKING FUTURE PERFECT CONTINUOUS==========")
    sentence = "They will have been going there for three days by that time"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'5': 'FutPerfCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Will they have been trying to perform this stuff?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'5': 'FutPerfCont'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if PRINT_POSITIVE: print("==========THERE IS ARE==========")
    sentence = "There is a cat here"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'there_is_are','2':'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "There really are a lot of cats here"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'there_is_are','3':'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "There will really be a lot of people in the stadium"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'there_is_are','4':'FutSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "Will there really be many of them?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'2': 'there_is_are','4':'FutSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "The friends will be there"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4':'FutSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    if args.show_known_errors:
        #been inside NP while other markers are inside VP
        sentence = "There will have been a lot of cars in the garage"
        map, gr_log, voc_log = get_map(sentence, model)
        ideal_gram = {'1': 'there_is_are','4':'FutPerf'}
        ideal_voc = {}
        if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
        assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
        if PRINT_POSITIVE: print()

    sentence = "There have been many friends"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1':'there_is_are', '3':'PrPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========GERUND==========")
    sentence = "I like going there"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'2': 'PresSimp','3':'Gerund'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    sentence = "Does he hate skiing?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PresSimp','4':'Gerund'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========Have_TO==========")
    sentence = "I have to go there"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'modal_have_to', '2': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    sentence = "Does he have to attend school?"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'5': 'modal_have_to', '3': 'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========PHRASAL VEBRS==========")
    sentence = "I WANT TO GIVE UP SMOKING"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'2': 'PresSimp'}
    ideal_voc = {'4': 'phrasal_verb', '5': 'phrasal_verb'}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    sentence = "You have to turn this ugly light off"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'2': 'PresSimp','4': 'modal_have_to'}
    ideal_voc = {'4': 'dist_phrasal_verb', '8': 'dist_phrasal_verb'}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if args.show_known_errors:
        #Доработать фразовые глаголы с to be
        sentence = "Why are you upset"
        map, gr_log, voc_log = get_map(sentence, model)
        ideal_gram = {'2': 'PresSimp'}
        ideal_voc = {'2': 'dist_phrasal_verb', '4': 'dist_phrasal_verb'}
        if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
        assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
        if PRINT_POSITIVE: print()

    sentence = "Who has kicked him out"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PrPerf'}
    ideal_voc = {'3': 'phrasal_verb', '5': 'phrasal_verb'}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    sentence = "You will have to let this big fat boss in"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'FutSimp','5':'modal_have_to'}
    ideal_voc = {'5': 'dist_phrasal_verb', '10': 'dist_phrasal_verb'}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========CONDITIONAL_0==========")
    sentence = "IF I HAVE MONEY I GO TO CLUB"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'ZeroCond','3':'PresSimp','6':'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    sentence = "If he doesn't have much time he brings food from somewhere else"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'ZeroCond','5':'PresSimp','9':'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    sentence = "They normally start talking when the teacher goes out of the class"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'5': 'ZeroCond','3':'PresSimp','4':'Gerund','8':'PresSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========CONDITIONAL_1==========")
    sentence = "If I am hungry, I will get something to eat"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'FirstCond','3':'PresSimp','8':'FutSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
    
    sentence = "I will bring a blanket,  if it is that cold"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'7': 'FirstCond','9':'PresSimp','3':'FutSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========CONDITIONAL_2==========")
    if args.show_known_errors:
        #did оказывается в одном поддереве с go и триггерится вопрос в Past simple
        sentence = "If I did that, I would go away"
        map, gr_log, voc_log = get_map(sentence, model)
        ideal_gram = {'1': 'SecondCond','3':'PastSimp'}
        ideal_voc = {}
        if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
        assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
        if PRINT_POSITIVE: print()

    sentence = "If I had that, I would go away"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'SecondCond','3':'PastSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    sentence = "These guys would enjoy if they had time"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'5': 'SecondCond','7':'PastSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========CONDITIONAL_3==========")
    sentence = "If he had talked to me, I would have listened to him"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'1': 'ThirdCond','4':'PastPerf','11': 'would_have_V3'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    sentence = "You would have won the prize, if you had participated in the competition"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'8': 'ThirdCond','4':'would_have_V3','11': 'PastPerf'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========PRESENT SIMPLE PASSIVE==========")
    sentence = "I am informed about this sitation and will start troubleshooting right now"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PresSimp_Passive', '9':'FutSimp', '10':'Gerund'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    sentence = "This company is sponsored by government"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PresSimp_Passive'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========PAST SIMPLE PASSIVE==========")
    sentence = "I was informed about this sitation and will start troubleshooting right now"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'3': 'PastSimp_Passive', '9':'FutSimp', '10':'Gerund'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========FUT SIMPLE PASSIVE==========")
    sentence = "I will be brought to the stadium by my bus"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'FutSimp_Passive'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========Present cont  PASSIVE==========")
    sentence = "I am being terrified by pixies"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PresCont_Passive'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========Past cont  PASSIVE==========")
    sentence = "I was being terrified by pixies"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'4': 'PastCont_Passive'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========Pres Perf  PASSIVE==========")
    sentence = "This house has already been built"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'6': 'PrPerf_Passive'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========Past Perf  PASSIVE==========")
    sentence = "This house had been built before I came"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'5': 'PastPerf_Passive','8':'PastSimp'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()

    if PRINT_POSITIVE: print("==========Fut Perfect  PASSIVE==========")
    sentence = "This house will have been built by January"
    map, gr_log, voc_log = get_map(sentence, model)
    ideal_gram = {'6': 'FutPerf_Passive'}
    ideal_voc = {}
    if PRINT_POSITIVE: print("NOW CHECKING <", sentence, ">")
    assert_analysis_results(gr_log, voc_log, ideal_gram, ideal_voc, sentence)
    if PRINT_POSITIVE: print()
test()