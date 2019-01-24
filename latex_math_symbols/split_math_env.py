import re



ignore_characters = ['\;']





""""#######                                                                           #########
### Adapted from https://github.com/alvinwan/TexSoup/blob/master/TexSoup/reader.py#L9   ###
#######                                                                           #########

COMMAND_TOKENS = {'\\'}
MATH_TOKENS = {'$', '\[', '\]', '\(', '\)'}
COMMENT_TOKENS = {'%'}
ARG_START_TOKENS = {'[', '{'}
ARG_END_TOKENS = {']', '}'}
ARG_TOKENS = ARG_START_TOKENS | ARG_END_TOKENS
ALL_TOKENS = COMMAND_TOKENS | ARG_TOKENS | MATH_TOKENS | COMMENT_TOKENS
SKIP_ENVS = ('verbatim', 'equation', 'lstlisting', 'align', 'alignat',
             'equation*', 'align*', 'math', 'displaymath', 'split', 'array',
             'eqnarray', 'eqnarray*', 'multline', 'multline*', 'gather',
             'gather*', 'flalign', 'flalign*',
             '$', '$$', '\[', '\]', '\(', '\)')
BRACKETS_DELIMITERS = {'(', ')', '<', '>', '[', ']', '{', '}',
                       '\{', '\}', '.' '|', '\langle', '\rangle',
                       '\lfloor', '\rfloor', '\lceil', '\rceil',
                       r'\ulcorner', r'\urcorner', '\lbrack', '\rbrack'}
SIZE_PREFIX = ('left', 'right', 'big', 'Big', 'bigg', 'Bigg')
PUNCTUATION_COMMANDS = {command + bracket
                        for command in SIZE_PREFIX
                        for bracket in BRACKETS_DELIMITERS.union({'|', '.'})}"""

capure = []



"""
How to handle subscripts? (ignore)
"""

e_1 = "{{B_s^2}\over{4 \pi ( \\rho_n+\\rho_I )}}"

e_2 = "10^4\;K"

print(e)