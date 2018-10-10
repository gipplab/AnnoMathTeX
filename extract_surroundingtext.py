#import section
from bs4 import BeautifulSoup
import re
from os import listdir
from os.path import isfile, join
import pickle
from operator import itemgetter
from collections import OrderedDict

#global path
mypath = "F:\\arXiv"

################################################################
# CONSTRUCT CATALOG WITH TEXT SURROUNDING THE IDENTIFIER FORMULA
################################################################

annotation_catalog = {}
# with open(mypath + "\\output2\\" + "annotation_catalog.pkl", "rb") as f:
#     annotation_catalog = pickle.load(f)

print("")

###########################
# DEFINE (GLOBAL) FUNCTIONS
###########################

#annotation extraction
def extract_annotations (file,filename,annotation_catalog):
    #extract formulae from file
    fileString = file.read()
    formulae = BeautifulSoup(fileString,'html.parser').find_all('formula')

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
            #formulaString
            s = str(formula.contents)
            start = 'alttext="'
            end = '" display='
            try:
                TeX = re.search('%s(.*)%s' % (start, end), s).group(1)
            except:
                TeX = ""

            # extract surrounding tex
            index = fileString.find('alttext="' + TeX + '" display=')
            surrounding_text = fileString[index-500:index+500]

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

# filenumber
flnr = 0
# excluded files
excl = 0

for dir in listdir(mypath + "\\NTCIR12"):

    #open data
    onlyfiles = [f for f in listdir(mypath + "\\NTCIR12\\" + dir) if isfile(join(mypath + "\\NTCIR12\\" + dir, f))]

    for filename in onlyfiles:
        flnr += 1
        fullpath = mypath + "\\NTCIR12\\" + dir + "\\" + filename
        print("Processing document #" + str(flnr) + " = " + str(round(flnr/(onlyfiles.__len__()-excl)*100,1)) + " % :")
        print(fullpath)

        file = open(fullpath, "r", encoding="utf8")
        annotation_catalog = extract_annotations(file,filename,annotation_catalog)

        f = open(mypath + "\\output2\\" + "annotation_catalog.pkl", "wb")
        pickle.dump(annotation_catalog, f)
        f.close()

print("Total processed " + str(flnr) + " documents.")

print("end")