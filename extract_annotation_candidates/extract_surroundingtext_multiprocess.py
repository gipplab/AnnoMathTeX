#import section
from bs4 import BeautifulSoup
import re
from os import listdir
from os.path import isfile, join
import pickle
from operator import itemgetter
from collections import OrderedDict
import multiprocessing
import time

#global path
mypath = "F:\\arXiv"

################################################################
# CONSTRUCT CATALOG WITH TEXT SURROUNDING THE IDENTIFIER FORMULA
################################################################

# annotation_catalog = {}
# with open(mypath + "\\output2\\" + "annotation_catalog.pkl", "rb") as f:
#     annotation_catalog = pickle.load(f)

# annotation_candidates = {}
# with open(mypath + "\\output2\\" + "annotation_candidates.pkl", "rb") as f:
#     annotation_candidates = pickle.load(f)

#print("")

###########################
# DEFINE (GLOBAL) FUNCTIONS
###########################

#annotation extraction
def extract_annotations (file,filename):
    annotation_catalog = {}

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

def process_files(dir):
    annotation_catalog = {}
    onlyfiles = [f for f in listdir(dir)]
    for filename in onlyfiles:
        fullpath = dir + "\\" + filename
        print(fullpath)
        file = open(fullpath, "r", encoding="utf8")
        annotation_catalog.update(extract_annotations(file,filename))
        file.close()
    return annotation_catalog

#################
# MULTIPROCESSING
#################

if __name__ == '__main__':
    t1 = time.time()
    annotation_catalog = {}
    tmp_catalogs = {}

    # open data
    path = mypath + "\\NTCIR12"
    # dir_list = [path + "\\0001", path + "\\0002"]
    dir_list = []
    for dir in listdir(path):
        dir_list.append(path + "\\" + dir)

    with multiprocessing.Pool() as p:
        try:
            tmp_catalogs = p.map(process_files, [dir for dir in dir_list])
        except:
            pass
    for catalog in tmp_catalogs:
        for identifier in catalog.items():
            try:
                annotation_catalog[identifier[0]].update(identifier[1])
            except:
                annotation_catalog[identifier[0]] = identifier[1]

    f = open(mypath + "\\output2\\" + "annotation_catalog.pkl", "wb")
    pickle.dump(annotation_catalog, f)
    f.close()

    t2 = time.time()
    print(t2-t1)

print("end")