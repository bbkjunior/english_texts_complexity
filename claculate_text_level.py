



sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def calculate_text_level(raw_text, print_debug_message = False):
    processed_text = punct_setnence_lower(raw_text,sent_detector)
    
    grammar_map = get_sent_gramm_features_map(processed_text)
    
    text_lemm = get_lemm_text(grammar_map)
    
    tf_idf_dict = get_tf_idf_dict(text_lemm)
    
    weights = get_weights_empty_list(grammar_map)
    
    weights = get_difficult_grammar(grammar_map,test_weights, debug = print_debug)
    weights = get_phrasal_verbs(grammar_map,test_weights, debug = print_debug)
    weights = assign_tf_idf(grammar_map,test_weights, debug = print_debug)
    
    easy, difficult = split_into_groups(weights)
    
    calculate_level(easy, difficult,  debug = print_debug)