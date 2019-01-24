import os
import re
import json


"""
Have to extract the parts of math environment. 
Is it necessary to recognize what parts there are?
    - yes, for identifier recognition
    - maybe, for formula recognition
        - if several formulae are in the same math environment (on the same line)
        
        
Useful: 
    - Source code to 'the not so short introduction to latex': https://github.com/oetiker/lshort
    - List of latex mathematical symbols (incomplete): https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols
    
BETTER: Construct rules, by which the strings are split into their parts
"""



file_names = [f for f in os.listdir(os.getcwd()) if not f.endswith('.py') and not f.endswith('.json')]



split_symbols = ['delimiters', 'relational_operators',
                 'binary_operators', 'set_and_or_logic_notation',
                 'arrows', 'unary_operators', 'negated_binary_operators']

all_others = [f for f in file_names if f not in split_symbols]





def extract_symbols(file_names):
    symbol_dict = {}
    symbol_list = []
    for file_name in file_names:
        path = os.getcwd() + '/' + file_name
        with open(path, 'r') as file:
            lines = file.read()#.splitlines()

        symbols = re.findall(r'(?<=<math>).*?(?=</math)', lines)

        symbol_dict[file_name] = symbols
        symbol_list += symbols

    return symbol_dict, symbol_list



def write_to_json(symbol_dict):
    with open('latex_math_symbols.json', 'w') as outfile:
        json.dump(symbol_dict, outfile)


#for k in symbol_dict:
#    print(k, symbol_dict[k])


_, _split = extract_symbols(split_symbols)


split_string = '|'.join('({})'.format(c) for c in _split)
split_string += '|(\W)'
print(split_string)

e_1 = "{{B_s^2}\over{4 \pi ( \\rho_n+\\rho_I )}}"


