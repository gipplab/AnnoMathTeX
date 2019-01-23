import os
import re
import json

file_names = [f for f in os.listdir(os.getcwd()) if not f.endswith('.py')]



symbol_dict = {}
symbol_list = []

for file_name in file_names:
    path = os.getcwd() + '/' + file_name
    with open(path, 'r') as file:
        lines = file.read()#.splitlines()

    symbols = re.findall(r'(?<=<math>).*?(?=</math)', lines)

    symbol_dict[file_name] = symbols
    symbol_list += symbols



def write_to_json(symbol_dict):
    with open('latex_math_symbols.json', 'w') as outfile:
        json.dump(symbol_dict, outfile)


