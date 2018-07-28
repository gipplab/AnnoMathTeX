#from bs4 import BeautifulSoup
from TexSoup import TexSoup
import re

def extract_formulae(document):

    #soupify document
    soup = TexSoup(document)

    #find all formulae within 'equation', 'align',  and '$' environment
    #strip them from their tags / macros
    equations = list(soup.find_all('equation'))
    for i in range(0,len(equations)):
        equations[i] = str(equations[i]).replace('\\begin{equation}','').replace('\\end{equation}','')
    aligns = list(soup.find_all('align'))
    for i in range(0,len(aligns)):
        aligns[i] = str(aligns[i]).replace('\\begin{align}','').replace('\\end{align}','')
    maths = list(soup.find_all('$'))
    for i in range(0,len(maths)):
        maths[i] = str(maths[i]).replace('$','')

    #create and return joint formula list
    formulae = equations + aligns + maths

    return formulae