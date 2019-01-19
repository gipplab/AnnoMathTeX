from io import StringIO
import tokenize
from pyparsing import *


"""f = "\[ x^n + y^n = z^n \]"

#print([token[1] for token in tokenize.generate_tokens(StringIO(f).readline) if token[1]])

# grammar definition
commandname = Word(alphas)
leftbrace = Literal("{")
rightbrace = Literal("}")
parameter = Word(alphas)
command = Literal("\\") + commandname + leftbrace + parameter + rightbrace

# input string
mystring = "\section{hello}"

# parse input string
print(mystring, "->", command.parseString(f))"""


import urllib2
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
infile = opener.open('http://en.wikipedia.org/w/index.php?title=Albert_Einstein&printable=yes')
page = infile.read()
