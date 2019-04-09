import json
import os
import re


class CustomMathEnvParser:

    def __init__(self, formula):
        self.formula = formula

    #r = re.compile(r'(?i)\b[a-z]\b|(?<=_)[a-z]|(?<=[^a-z])[a-z](?=_)')
    #s = r'\underset{\mathbf{S}} {\operatorname{arg\,min}}  \sum_{i=1}^{k} \sum_{\mathbf x \in S_i} '

    def load_math_symbols(self):
        #change when integrating into project
        path = os.getcwd() + '/parsing/mathhandling/latex_math_symbols.json'
        with open(path, 'r') as f:
            s = f.read()

        all_dict = json.loads(s)
        keys = list(all_dict.keys())
        all_symbols = [s.replace('\\', '\\\\') for key in keys for s in all_dict[key]]
        all_symbols_string = '|'.join(all_symbols)
        all_symbols_string = r'({})'.format(all_symbols_string)
        return all_symbols_string

    def get_id_pos_len(self):
        #all_symbols = self.load_math_symbols()
        r = re.compile(r'(\b[a-z]\b|(?<=_)[a-z]|(?<=[^a-z])[a-z](?=_))', re.IGNORECASE)
        #identifiers = re.findall(r, self.formula, re.IGNORECASE)
        id_pos_len = [(i.group(), i.start(), len(i.group())) for i in r.finditer(self.formula)]
        return id_pos_len


    def get_split_math_env(self):
        id_pos_len = self.get_id_pos_len()
        split_math_env = []
        identifiers = []
        last_pos = 0
        for id, p, l in id_pos_len:
            formula_chunk = self.formula[last_pos:p]
            split_math_env.append(formula_chunk)
            split_math_env.append(id)
            identifiers.append(id)
            last_pos = p+l


        return identifiers, split_math_env

if __name__ == "__main__":
    s = r'$ \underset{\mathbf{ S }} {\operatorname{arg\,min}} \sum_{ i =1}^{ k } \sum_{\mathbf x \ i n S _ i } \left\| \mathbf x - \boldsymbol\mu_ i \r i ght\|^2 = \underset{\mathbf{ S }} {\operatorname{arg\,m i n}} \sum_{ i =1}^{ k } | S _ i | \operatorname{Var} S _ i $'
    #s = r'$ \underset{\mathbf{ S }} {\operatorname{arg\,min}} \sum_{ i =1}^{ k }'
    c = CustomMathEnvParser(s)
    identifiers = c.get_id_pos_len()
    split_math_env = c.get_split_math_env()
    print(identifiers)
    print(split_math_env)

