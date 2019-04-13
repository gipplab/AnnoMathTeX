import json
import os
import re


class CustomMathEnvParser:
    """
    This class is used to extract the identifiers from a formula and split the formula into parts.
    E.g. the formula 'm ^{( t +1)}_ i' would be split into ['m', ' ^{( ', 't', ' +1)}_ ', 'i] with 'm', 't', and 'i'
    being the identifiers and the rest of the string being symbols that will not be highlighted.
    """

    def __init__(self, math_env):
        """
        :param math_env: The math environment that is being parsed.
        """
        self.math_env = math_env

    def load_math_symbols(self):
        """
        Not used right now. latex_math_symbols.json is a file that contains a lot of latex commands. The idea was to
        use those to split the math environment. However, I took a different approache now: Extracting the identifiers
        and splitting the math environemnt on those.
        :return: A string of all symbols contained in latex_math_symbols.json that can be used as a regex to split the
                 math environment.
        """
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
        """
        This method extracts the identifiers from a math environment using a regex. In addition the position of each identifier
        and it's length is added to a triple, which is used in get_split_math_env() to split the entire math
        environment into the identifiers and non identifier parts.
        :return: A triple of the identifier, the position of the identifier in the string and the length of the
                 identifier.
        """
        r = re.compile(r'(\b[a-z]\b|(?<=_)[a-z]|(?<=[^a-z])[a-z](?=_))', re.IGNORECASE)
        id_pos_len = [(i.group(), i.start(), len(i.group())) for i in r.finditer(self.math_env)]
        return id_pos_len


    def get_split_math_env(self):
        """

        This mehtod splits the entire math environemnt the identifier and non identifier parts. These are used in the
        Parser class to construct Identifier and Formula Objects from the math environment.
        :return: The identifiers as a list and the entire math environment (also containing the identifiers) as a list.
        """
        id_pos_len = self.get_id_pos_len()
        split_math_env = []
        identifiers = []
        last_pos = 0
        for id, p, l in id_pos_len:
            formula_chunk = self.math_env[last_pos:p]
            split_math_env.append(formula_chunk)
            split_math_env.append(id)
            identifiers.append(id)
            last_pos = p+l

        end_chunk = self.math_env[last_pos:]
        split_math_env.append(end_chunk)
        return identifiers, split_math_env



if __name__ == "__main__":
    """
    Used for testing purposes
    """
    s = r'$ \underset{\mathbf{ S }} {\operatorname{arg\,min}} \sum_{ i =1}^{ k } \sum_{\mathbf x \ i n S _ i } \left\| \mathbf x - \boldsymbol\mu_ i \r i ght\|^2 = \underset{\mathbf{ S }} {\operatorname{arg\,m i n}} \sum_{ i =1}^{ k } | S _ i | \operatorname{Var} S _ i $'
    s1 = r'$\Delta(m,n,x) =  \phi(S_n) + \phi(S_m) - \phi(S_n \backslash \{ x \} ) - \phi(S_m \cup \{ x \} )$'
    s2 = r'$n,m \in \{1 \cdots k \}</math> and <math>x \in S_n$'
    #s = r'$ \underset{\mathbf{ S }} {\operatorname{arg\,min}} \sum_{ i =1}^{ k }'
    c = CustomMathEnvParser(s2)
    #identifiers = c.get_id_pos_len()
    identifiers, split_math_env = c.get_split_math_env()
    print(identifiers)
    print(split_math_env)

