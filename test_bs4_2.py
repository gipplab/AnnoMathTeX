from bs4 import BeautifulSoup
import re
import os
from math_test import FormulaSplitter
import warnings
warnings.filterwarnings("ignore")


def read_file():
    filepath = '/Users/ianmackerracher/PycharmProjects/AnnoMathTeX/evaluation/Bose-Einstein_condensate.html'
    with open(filepath, 'r') as f:
        file = f.read()

    return file

def extract_formula():
    file = read_file()
    soup = BeautifulSoup(file)
    formula = None
    for tag in soup.find_all():
        if tag.name == 'math':
            annotation = tag.find("annotation", {"encoding": "application/x-tex"})
            formula = annotation.contents[0]
            #formula = re.sub(r'^\s\s*', '', formula)
            #formula = re.sub(r'\s\s*$', '', formula)
            break

    return formula



formula6 = "T_{c}=\\frac{n}{\\zeta(3/2)}"
formula = extract_formula()
fs = FormulaSplitter(formula6)
processed_formula = fs.get_identifiers()
print(processed_formula)

