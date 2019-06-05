from calculate_level_new import get_features, calculate_level, get_map
from ud_class import Model

import argparse

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-s', '--show_output', action='store_true')
parser.add_argument('-f','--file', help='path to the file with raw text')
args = parser.parse_args()


model = Model('./UDPIPE/english-ud-2.0-170801.udpipe')

text = ''
with open(args.file, "r", encoding = "utf-8") as text_file:
    for line in text_file.readlines():
        text += line + ' '
text_analysis_map, level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight = get_map(text, model)

show_out = args.show_output
if show_out:
    for sentence in text_analysis_map[0]:
        for word in sentence:
            print(word,'\n')
        print("====================")
    print('\n\n')
#get_features(level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight)
level = calculate_level(level_collected_vocab, level_collected_weight, level_collected_gramm, level_grammar_collected_weight, show_output = args.show_output)

print (level)