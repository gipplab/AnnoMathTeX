#from TexSoup import TexSoup
import TexSoup
import os
import pprint
from collections import Iterable


with open(os.getcwd() + '/latexfiles/dgani_small.tex', 'r') as f:
    file = f.read()


#soup = TexSoup(file)


def process(x):
    print(type(x))

f = []

def flatten(collection):
    for x in collection:
        #print(x)
        if isinstance(x, Iterable) and not isinstance(x, str):
            #yield from flatten(x)
            f.append(flatten(x))
            #print(x)
        else:
            #yield x
            #print(x)
            #return x
            process(x)
            f.append(x)

def extract(data):
    yield from (x for x in flatten(data))


math_env_markers = ['$', '$$', '\\[', '\\(', '\\begin{equation}', '\\begin{align}']


def everything(tex_tree):
    result = []
    for tex_code in tex_tree:
        if isinstance(tex_code, TexSoup.TexEnv):
            #print(tex_code)
            r = [tex_code.begin + str(tex_code.arguments), everything(tex_code.everything), tex_code.end]
            result.append(r)
            #print(*flatten(r))
            #print(str(tex_code.arguments))
            #print(*tex_code.everything)

        elif isinstance(tex_code, TexSoup.TexCmd):
            result.append(["\\" + tex_code.name + str(tex_code.arguments)])
        elif isinstance(tex_code, TexSoup.TokenWithPosition):
            #print(tex_code.position)
            print(tex_code.text)
            result.append(tex_code.text)
        elif isinstance(tex_code, TexSoup.Arg):
            #print(tex_code)
            result.append(["{", everything(TexSoup.TexSoup(tex_code.value).expr.everything), "}"])
        else:
            #result.append(('TEXT', [str(tex_code)]))
            result.append('TTTTT')

    return result




tex_soup = TexSoup.TexSoup(file)
tex_text = everything(tex_soup.expr.everything)




#print(flatten(tex_text))

#flatten(tex_text)
#print(f)


#print(*extract(tex_text))
#print(*flatten(tex_text))

#for i in tex_soup:
#    print(i.find_all('equation'))


