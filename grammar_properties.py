from vocabulary import phrasal_list_big

def get_verb_phrase_properties(verb_phrases_dict,grammar_properties_log,pos_word_dict,vocab_properties_log):
    conditional_list = []
    for head_of_subtree_plus_index, dependent_elements in verb_phrases_dict.items():
            head_of_subtree_index = head_of_subtree_plus_index.split("_")[0]
            continious = False
            head_word_lower = head_of_subtree_plus_index.split("_")[1].lower()
            head_lemma_lower = head_of_subtree_plus_index.split("_")[2].lower()
            #print(pos_word_dict[head_of_subtree_index][1])
            if(head_word_lower.endswith("ing") and 'VerbForm=Inf' not in pos_word_dict[head_of_subtree_index][1][3]):
                continious = True  
            be_words = ['am','is','are',"was","were","'s","'re","'m"]
            present_be = ['am','is','are',"'s","'re","'m"]
            past_be = ["was","were"]
            aux_be_words = ['been','be']
            be_head = None
            be_non_head = None
            aux_be_head = None
            if(head_word_lower in be_words):
                be_head = head_word_lower
            elif(head_word_lower in aux_be_words):
                aux_be_head = head_of_subtree_index
                #print("AUX detected")
            have_words = ["have","has","had","'ve"]
            have_head = False
            if(head_word_lower in have_words):
                have_head = head_word_lower
                
            head_inf = False
            if head_word_lower == head_lemma_lower: head_inf = True
            would_Vinf_index = -1
            
            head_type = pos_word_dict[head_of_subtree_index][1][2]
            head_V3 = False
            head_V2 = False
            if(head_type == "VBN"):
                head_V3 = True
            elif(head_type == "VBD"):
                head_V2 = True
            would_V3_index = -1
            
            being = False
        
            perfect = False
            future = False
            
            past_perf = False
            
            conditional_if_index = -1
            conditional_when_index = -1
            present_index =  -1
            past_index = -1
            future_index = -1
            
            another_tense_assigned_inside_subtree = False
            for dep_el in dependent_elements:
                #print("dep_el",dep_el)
                #print(be_head,int(head_of_subtree_index), int(dep_el[0]))
                #if(be_head and dep_el[1].lower() == "there" and int(head_of_subtree_index)  > int(dep_el[0]) ):
                #подразумевается что в случае smth is there - будет именная фраза
                
                #for passive voice
                #print("be_words",be_words, dep_el[1].lower,dep_el[1].lower() in be_words)
                if(dep_el[1].lower() in be_words or dep_el[1].lower() in aux_be_words):
                    be_non_head = dep_el[1].lower()
                elif(dep_el[1].lower() == "being"):
                    being = True
                
                #GERUND
                #print(dep_el[5])
                if "VerbForm=Ger" in dep_el[5] or dep_el[1].endswith("ing"):#грубое округление с расчетом на то что не герундиев оканчивающихся на инг мало
                    if (len(dep_el[1])>4 and not head_V3 and not head_V2 and dep_el[3] != 'PRON'):#доп филтрр от коротких существительных
                        grammar_properties_log[dep_el[0]] = "Gerund"
                
                potential_phrasal_verb = head_lemma_lower + ' ' + dep_el[2]
                #print("potential_phrasal_verb",potential_phrasal_verb)
                """
                if( potential_phrasal_verb in  phrasal_list_EASY):
                    #print("EASY PV DETECTED")
                    if abs(int(dep_el[0]) - int(head_of_subtree_index)) > 2:
                        vocab_properties_log[dep_el[0]] = "dist_easy_phrasal_verb"
                        vocab_properties_log[head_of_subtree_index] = "dist_easy_phrasal_verb"
                    else:
                        vocab_properties_log[dep_el[0]] = "easy_phrasal_verb"
                        vocab_properties_log[head_of_subtree_index] = "easy_phrasal_verb"
                """
                if(potential_phrasal_verb in phrasal_list_big):
                    if abs(int(dep_el[0]) - int(head_of_subtree_index)) > 2:
                        vocab_properties_log[dep_el[0]] = "dist_phrasal_verb"
                        vocab_properties_log[head_of_subtree_index] = "dist_phrasal_verb"
                    else:
                        vocab_properties_log[dep_el[0]] = "phrasal_verb"
                        vocab_properties_log[head_of_subtree_index] = "phrasal_verb"
                
                if(be_head and dep_el[1].lower() == "there"):
                    grammar_properties_log[dep_el[0]] = "there_is_are"
                elif(aux_be_head and dep_el[1].lower() == "there" and int(aux_be_head) > int(dep_el[0])):
                    grammar_properties_log[dep_el[0]] = "there_is_are"
                elif(be_head in past_be and dep_el[1].lower().endswith("ing")):
                    grammar_properties_log[dep_el[0]] = "PastCont"
                    another_tense_assigned_inside_subtree = True
                elif(have_head and "Tense=Past" in dep_el[5]):
                    if(have_head == "has" or have_head == "has"):
                        grammar_properties_log[dep_el[0]] = "PrPerf"
                        another_tense_assigned_inside_subtree = True
                    elif(have_head == "had" and 'VerbForm=Inf' not in pos_word_dict[head_of_subtree_index][1][3]):
                        grammar_properties_log[dep_el[0]] = "PastPerf"
                        another_tense_assigned_inside_subtree = True
                    
                if(dep_el[1].lower() == "when"):
                    conditional_when_index = dep_el[0] 
                if(dep_el[1].lower() == "if"):
                    conditional_if_index = dep_el[0]
                if(dep_el[1].lower() == "would" and head_inf):
                    would_Vinf_index = dep_el[0]
                elif(dep_el[1].lower() == "would" and head_V3):
                    would_V3_index = dep_el[0]
                if (dep_el[3] == "VERB" and "VerbForm=Inf" in dep_el[5] and head_lemma_lower == "have"):
                    grammar_properties_log[dep_el[0]] = "modal_have_to"
                                    

                if (dep_el[1].lower() == "am" or dep_el[1].lower() == "is" or dep_el[1].lower() == "are"):
                    if (continious):
                        grammar_properties_log[head_of_subtree_index] = "PresCont"
                elif(dep_el[1].lower() == "was" or dep_el[1].lower() == "were"):
                    if (continious):
                        grammar_properties_log[head_of_subtree_index] = "PastCont"
                elif(dep_el[1].lower() == "will" or dep_el[1].lower() == "shall"):
                    future = True
                    future_index = dep_el[0]
                elif(dep_el[1].lower() == "had" and 'VerbForm=Inf' not in pos_word_dict[head_of_subtree_index][1][3]):
                    if(continious):
                        grammar_properties_log[head_of_subtree_index] = "PastPerfCont"#had (been) doing
                    else:
                        grammar_properties_log[head_of_subtree_index] = "PastPerf"
                        past_perf = True
                elif(dep_el[1].lower() == "have" or dep_el[1].lower() == "has" or dep_el[1].lower() == "'ve"): 
                    perfect = True
                    if(continious):
                        grammar_properties_log[head_of_subtree_index] = "PrPerfCont"
                    elif(would_V3_index == -1  and (head_V3 or head_V2)):
                        grammar_properties_log[head_of_subtree_index] = "PrPerf"
                    elif(int(would_V3_index) > 0):
                        grammar_properties_log[head_of_subtree_index] = "would_have_V3"
                        grammar_properties_log["would_have_V3"] = head_of_subtree_index
                elif(dep_el[1].lower() == "do" or dep_el[1].lower() == "does"):
                    grammar_properties_log[head_of_subtree_index] = "PresSimp"
                    present_index = dep_el[0]
                elif(dep_el[1].lower() == "did"):
                    grammar_properties_log[head_of_subtree_index] = "PastSimp"
                    past_index = dep_el[0]
                elif(dep_el[1].lower() == "would" and head_word_lower == "like"):
                    grammar_properties_log[head_of_subtree_index] = "would_like"
            if(be_non_head == "been" and past_perf and (head_V3 or head_V2)):
                grammar_properties_log[head_of_subtree_index] = "PastPerf_Passive"
            elif(be_non_head == "been" and perfect and (head_V3 or head_V2) and not future):
                grammar_properties_log[head_of_subtree_index] = "PrPerf_Passive"
            elif(be_non_head == "been" and perfect and (head_V3 or head_V2) and future):
                grammar_properties_log[head_of_subtree_index] = "FutPerf_Passive"
            elif (continious and future and perfect):
                grammar_properties_log[head_of_subtree_index] = "FutPerfCont"
            elif (continious and future):
                grammar_properties_log[head_of_subtree_index] = "FutCont"#определеит даже без will BE
            elif (perfect and future):
                grammar_properties_log[head_of_subtree_index] = "FutPerf"
            elif(future and not head_V2 and not head_V3):
                grammar_properties_log[head_of_subtree_index] = "FutSimp"
            #print("head_prop", pos_word_dict[head_of_subtree_index])    
            if(head_of_subtree_index not in grammar_properties_log and not another_tense_assigned_inside_subtree):#если нет вспомогательных маркеров
                head_properties = pos_word_dict[head_of_subtree_index]
                if ("Tense=Pres" in head_properties[1][3] ):
                    grammar_properties_log[head_of_subtree_index] = "PresSimp"
                    present_index = dep_el[0]
                elif("Tense=Past" in head_properties[1][3]):
                    if be_non_head:
                        if be_non_head in present_be and not being:
                            grammar_properties_log[head_of_subtree_index] = "PresSimp_Passive" 
                        elif be_non_head in present_be and being:
                            grammar_properties_log[head_of_subtree_index] = "PresCont_Passive" 
                        elif be_non_head in past_be and not being:
                            grammar_properties_log[head_of_subtree_index] = "PastSimp_Passive" 
                        elif be_non_head in past_be and being:
                            grammar_properties_log[head_of_subtree_index] = "PastCont_Passive"
                        elif be_non_head == "be" and future:
                            grammar_properties_log[head_of_subtree_index] = "FutSimp_Passive"
                    else:
                        grammar_properties_log[head_of_subtree_index] = "PastSimp" 
                        past_index = dep_el[0]

                                 
                elif("Tense" not in head_properties[1][3] or head_of_subtree_index not in grammar_properties_log):
                    pass#print("FAILED TO DETECT VERB SUBTREE TENSE")
					
                   
            if int(present_index) > 0 and (int(conditional_if_index) > 0 or (int(conditional_when_index) > 0)):
                conditional_list.append((max(int(conditional_if_index),int(conditional_when_index)), "if_pres"))
            elif(int(conditional_if_index) > 0 and past_perf):
                conditional_list.append((conditional_if_index, "if_past_perfect"))
            elif(int(past_index) > 0 and int(conditional_if_index) > 0):
                conditional_list.append((conditional_if_index, "if_past"))
            elif(int(present_index) > 0 ):
                conditional_list.append((present_index, "pres"))
            elif(int(future_index) > 0 ):
                conditional_list.append((future_index, "future"))
            elif(int(would_Vinf_index) > 0 ):
                conditional_list.append((would_Vinf_index, "would_Vinf"))
            elif(int(would_V3_index) > 0 ):
                conditional_list.append((would_V3_index, "would_V3_index"))    
    #print("conditional_list",conditional_list)            
    if len(conditional_list) >1:
        if_past_perfect_index = None
        would_V3 = False
        
        if_past_index = None
        would_Vinf = False
        
        cond_word_index = None
        pres = False
        fut = False
        for condition_element in conditional_list:
            #standard sequence if/when then
            if(condition_element[1] == "if_pres"):
                cond_word_index = condition_element[0]
            elif(condition_element[1] == "if_past_perfect"):
                if_past_perfect_index = condition_element[0]
            elif(condition_element[1] == "pres"):
                pres = True
            elif(condition_element[1] == "future"):
                fut = True
            elif(condition_element[1] == "would_Vinf"):
                would_Vinf = True
            elif(condition_element[1] == "if_past"):
                if_past_index = condition_element[0]
            elif(condition_element[1] == "would_V3_index"):
                would_V3 = True    
                
        if(cond_word_index and pres):
            grammar_properties_log[str(cond_word_index)] = "ZeroCond"
        elif(cond_word_index and fut):
            grammar_properties_log[str(cond_word_index)] = "FirstCond"
        elif(if_past_index and would_Vinf):
            grammar_properties_log[str(if_past_index)] = "SecondCond"
        elif(if_past_perfect_index and would_V3):
            grammar_properties_log[str(if_past_perfect_index)] = "ThirdCond"
    elif(len(conditional_list) == 1):
        cond_word_index = None
        #print("SHORTTT")
        #print(conditional_list[0][1])
        if conditional_list[0][1] == "if_pres":
            #print("SHORTTT--")
            grammar_properties_log["if_pres"] = str(conditional_list[0][0])
        elif conditional_list[0][1] == "would_Vinf":
            grammar_properties_log["would_Vinf"] = str(conditional_list[0][0])
			
def get_non_verb_phrase_properties(non_verb_phrases_dict,grammar_properties_log,pos_word_dict,vocab_properties_log):
    """оцениваем линейно без отсылки к поддереву"""
    pr_simple_be = ["am", "is", "are"]
    past_simp_be = ["was","were"]
    perfect_list = ["have","has"]
    future_list = ["will","shall"]
    be_list = ["be", "been"]
    be_phrasal_list = ["after", "along","away","upset","down", "up"]
    modal_verbs_list = ['can','may','should','would']
    for head_of_subtree_plus_index, dependent_elements in non_verb_phrases_dict.items():
        perfect = False
        future = False
        be_index = -1
        
        past_perf = False
        when_condition_index = -1
        if_condition_index = -1
        present = False
        past = False
        #Catch there is_are
        there_index = -1 
        #modal verbs
        modal = None
        would = None
        for dep_el in dependent_elements:
            #catch modal verbs
            if (dep_el[1].lower() == "can"):
                modal_index = dep_el[0]
        
            #Catch there is_are
            if (dep_el[1].lower() == "there"):
                there_index = dep_el[0]
            if "VerbForm=Ger" in dep_el[5] or dep_el[1].endswith("ing"):#грубое округление с расчетом на то что не герундиев оканчивающихся на инг мало
                if (len(dep_el[1])>4 and dep_el[3] != "PRON"):#доп филтрр от коротких существительных
                    #print("GERUND FOUND")
                    grammar_properties_log[dep_el[0]] = "Gerund"
            if (dep_el[1].lower() in modal_verbs_list):
                modal = dep_el[0]
                if (dep_el[1].lower() == "would"):
                    would = True
            elif (dep_el[1].lower() == "if"):
                if_condition_index = dep_el[0]
            elif(dep_el[1].lower() == "when"):
                when_condition_index = dep_el[0]
            elif (dep_el[1].lower() in be_list):
                be_index = int(dep_el[0])
                if dep_el[1].lower() == "be" and would:
                    grammar_properties_log[dep_el[0]] = "would_Vinf"
                    grammar_properties_log["would_Vinf"] = dep_el[0]
                elif(dep_el[1].lower() == "been" and modal):
                    grammar_properties_log[dep_el[0]] = "would_have_V3"
                    grammar_properties_log["would_have_V3"] = dep_el[0]
            if(dep_el[1].lower() in be_phrasal_list and int(be_index) > 0 and int(be_index) < int(dep_el[0])):
                if abs(int(dep_el[0]) - int(be_index)) > 2:
                        vocab_properties_log[str(dep_el[0])] = "dist_phrasal_verb"
                        vocab_properties_log[str(be_index)] = "dist_phrasal_verb"
                else:
                    vocab_properties_log[str(dep_el[0])]= "phrasal_verb"
                    vocab_properties_log[str(be_index)] = "phrasal_verb"
            if (dep_el[1].lower() in pr_simple_be):
                grammar_properties_log[dep_el[0]] = "PresSimp"
                present = True
            elif (dep_el[1].lower() in past_simp_be):
                grammar_properties_log[dep_el[0]] = "PastSimp"
                past = True
            elif (dep_el[1].lower() in perfect_list):
                perfect = True
            elif (dep_el[1].lower() in future_list):
                future = True
            elif (dep_el[1].lower() == "had"):
                past_perf = True
                
        if (be_index > 0):            
            if (perfect and not future and not modal):
                grammar_properties_log[str(be_index)] = "PrPerf"
            elif (perfect and future):
                grammar_properties_log[str(be_index)] = "FutPerf"
            elif(not perfect and future):
                grammar_properties_log[str(be_index)] = "FutSimp"
            elif(past_perf):
                grammar_properties_log[str(be_index)] = "PastPerf"
            elif(modal):
                grammar_properties_log[str(be_index)] = "PresSimp"
                
            if(int(there_index) > 0 and int(there_index) < be_index):
                grammar_properties_log[str(there_index)] = "there_is_are"
        else:
           if(modal):
                grammar_properties_log[modal] = "PresSimp" 
                
                
        #print("if_condition_index",if_condition_index)         
        if((int(when_condition_index) > 0 or int(if_condition_index) > 0) and present):
            grammar_properties_log["if_pres"] = str(max(int(when_condition_index),int(if_condition_index)))            
        elif(int(if_condition_index) > 0 and past):
            grammar_properties_log["if_past"] = str(if_condition_index)
        elif(int(if_condition_index) > 0 and past_perf):
            grammar_properties_log["if_past_perf"] = str(if_condition_index)
        