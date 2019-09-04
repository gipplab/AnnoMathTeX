#import section
from bs4 import BeautifulSoup
import re
from os import listdir
from os.path import isfile, join
import pickle
from operator import itemgetter
from collections import OrderedDict

#global path
mypath = "C:\\Users\\Philipp\\Dropbox\\PhD\\Projects\\Annotation Recommender\\AnnoMathTeX\\evaluation"

################################################################
# CONSTRUCT CATALOG WITH TEXT SURROUNDING THE IDENTIFIER FORMULA
################################################################

annotation_catalog = {}
# with open(mypath + "\\" + "annotation_catalog.pkl", "rb") as f:
#     annotation_catalog = pickle.load(f)

print("")

###########################
# DEFINE (GLOBAL) FUNCTIONS
###########################

#annotation extraction
def extract_annotations (file,filename,annotation_catalog):
    #extract formulae from file
    fileString = file.read()
    formulae = BeautifulSoup(fileString,'html.parser').find_all('math')

    #extract formula components

    for formula in formulae:

        # utile function
        def findall(p, s):
            '''Yields all the positions of
            the pattern p in the string s.'''
            i = s.find(p)
            while i != -1:
                yield i
                i = s.find(p, i+1)

        # retrieve operators
        # operator counter
        onr = 0
        for i in findall('</m:mo', str(formula.contents)):
            onr += 1
        # retrieve identifiers
        # identifier counter
        inr = 0
        for i in findall('</m:mi', str(formula.contents)):
            inr += 1
        # retrieve numbers
        # number counter
        nnr = 0
        for i in findall('</m:mn',str(formula.contents)):
            nnr += 1

        # if formula small enough, retrieve it with surrounding text for annotation candidates
        if onr == 0 and inr <= 3 and nnr == 0:

            # extract TeX formula
            try:
                TeX = str(formula.contents[0])
            except:
                TeX = ""

            # extract surrounding tex
            index = fileString.find(TeX)
            surrounding_text = fileString[index-500:index+len(TeX)+500]

            try:
                annotation_catalog[TeX][filename] = surrounding_text
            except:
                annotation_catalog[TeX] = {}
                annotation_catalog[TeX][filename] = surrounding_text

    #close data
    file.close()
    return annotation_catalog

###############
# PROCESS FILES
###############

for filename in listdir(mypath):
    if filename.endswith(".txt"):

        fullpath = mypath + "\\" + filename
        print(fullpath)

        file = open(fullpath, "r")
        annotation_catalog = extract_annotations(file,filename,annotation_catalog)

        f = open(mypath + "\\" + "annotation_catalog.pkl", "wb")
        pickle.dump(annotation_catalog, f)
        f.close()

print("end")