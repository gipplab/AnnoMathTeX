from bs4 import BeautifulSoup
import os
import re

import warnings
warnings.filterwarnings("ignore")


def foo(request_file):
    soup = BeautifulSoup(request_file)
    #print(soup.prettify())
    #print(request_file.read())

    #for a in list(soup.find_all('math')):
    content = []
    for tag in list(soup.find_all()):
        if tag.name == 'math':
            annotation = tag.find("annotation", {"encoding": "application/x-tex"})
            formula = '${}$'.format(annotation.contents[0])
            content += ['\n', formula, '\n']
            #content.append('\n'*5)
        else:
            #content.append(tag)
            #print(tag.name)
            pass

    #new_math_tag = soup.new_tag('MATHNEW')
    #soup.math.replace_with(new_math_tag)

    for a in list(soup.find_all()):
        print(a)

    #for c in content:
    #    print(c)


def _find(request_file):
    soup = BeautifulSoup(request_file)

    math_envs = []
    while soup.find('math'):
        m = soup.find('math')
        formula = m.find("annotation", {"encoding": "application/x-tex"})
        #print(formula.contents[0])
        math_envs.append(formula.contents[0])
        #print(m)
        m.decompose()
        #break

    c = 0
    for t in list(soup.findAll('p')):
        #if re.search(r'^\s+$', t.content.string):
        natural_language = list(filter(lambda x: x != '\n', t.contents))
        if not natural_language:
            #placeholder for math tag
            #print(True, natural_language)
            #c += 1
            c += len(natural_language)
        #if len(t.text) == 2:
        #    c += 1
        #break


    #print(len(math_envs))
    #print(c)
    for m in math_envs:
        print(m)
        print()





def read_file(filepath):
    #filepath = '/Users/ianmackerracher/PycharmProjects/AnnoMathTeX/evaluation/Bose-Einstein_condensate.html'
    dirpath = '/Users/ianmackerracher/PycharmProjects/AnnoMathTeX/evaluation/'
    filepath = dirpath + filepath
    with open(filepath, 'r') as f:
        file = f.read()

    return file


d = os.getcwd() + '/evaluation'
filename = os.listdir(d)[0]#3 for small

request_file =  read_file(filename)

#request_file = re.sub(r'math.*?</math', r'\n\nMATH\n\n', request_file, flags=re.DOTALL)
_find(request_file)
