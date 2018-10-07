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

# annotation_catalog = {}
# with open(mypath + "\\output2\\" + "annotation_catalog.pkl", "rb") as f:
#     annotation_catalog = pickle.load(f)

#annotation_candidates = {}
with open(mypath + "\\output2\\" + "annotation_candidates.pkl", "rb") as f:
    annotation_candidates = pickle.load(f)

print("")

# #annotation extraction
# def extract_annotations (file,filename,annotation_catalog):
#     #extract formulae from file
#     fileString = file.read()
#     formulae = BeautifulSoup(fileString,'html.parser').find_all('formula')
#
#     #extract formula components
#
#     for formula in formulae:
#
#         # utile function
#         def findall(p, s):
#             '''Yields all the positions of
#             the pattern p in the string s.'''
#             i = s.find(p)
#             while i != -1:
#                 yield i
#                 i = s.find(p, i+1)
#
#         # retrieve operators
#         # operator counter
#         onr = 0
#         for i in findall('</m:mo', str(formula.contents)):
#             onr += 1
#         # retrieve identifiers
#         # identifier counter
#         inr = 0
#         for i in findall('</m:mi', str(formula.contents)):
#             inr += 1
#         # retrieve numbers
#         # number counter
#         nnr = 0
#         for i in findall('</m:mn',str(formula.contents)):
#             nnr += 1
#
#         # if formula small enough, retrieve it with surrounding text for annotation candidates
#         if onr == 0 and inr <= 3 and nnr == 0:
#
#             # extract TeX formula
#             #formulaString
#             s = str(formula.contents)
#             start = 'alttext="'
#             end = '" display='
#             try:
#                 TeX = re.search('%s(.*)%s' % (start, end), s).group(1)
#             except:
#                 TeX = ""
#
#             # extract surrounding tex
#             index = fileString.find('alttext="' + TeX + '" display=')
#             surrounding_text = fileString[index-500:index+500]
#
#             try:
#                 annotation_catalog[TeX][filename] = surrounding_text
#             except:
#                 annotation_catalog[TeX] = {}
#                 annotation_catalog[TeX][filename] = surrounding_text
#
#     #close data
#     file.close()
#     return annotation_catalog
#
# # filenumber
# flnr = 0
# # excluded files
# excl = 0
#
# for dir in listdir(mypath + "\\NTCIR12"):
#
#     #open data
#     onlyfiles = [f for f in listdir(mypath + "\\NTCIR12\\" + dir) if isfile(join(mypath + "\\NTCIR12\\" + dir, f))]
#
#     for filename in onlyfiles:
#         flnr += 1
#         fullpath = mypath + "\\NTCIR12\\" + dir + "\\" + filename
#         print("Processing document #" + str(flnr) + " = " + str(round(flnr/(onlyfiles.__len__()-excl)*100,1)) + " % :")
#         print(fullpath)
#
#         file = open(fullpath, "r", encoding="utf8")
#         annotation_catalog = extract_annotations(file,filename,annotation_catalog)
#
#         f = open(mypath + "\\output2\\" + "annotation_catalog.pkl", "wb")
#         pickle.dump(annotation_catalog, f)
#         f.close()
#
# print("Total processed " + str(flnr) + " documents.")

########################################################
# CONSTRUCT CATALOG WITH COUNTS OF ANNOTATION CANDIDATES
########################################################

# find surrounding words as annotation candidates

# exclude formulae and stopwords from candidates
excluded = [">", "<", "=", '"']
with open("output\\stopwords.txt") as f:
    stopwords = [line.strip() for line in f]
# only Latin and Greek letters
with open("output\\valid.txt") as f:
    valid = [line.strip() for line in f]

# list annotation candidate occurences for each identifier
for identifier in annotation_catalog.items():
    # exclude identifiers with indices
    #if not "_" in identifier[0] and not "^" in identifier[0]:
    # include only Latin and Greek letters
    if identifier[0] in valid:
        print("At identifier " + identifier[0])
        matches = {}
        # split candidate text sentence into words
        for candidate_text in identifier[1].values():
            words = candidate_text.split()
            for word in words:
                # lowercase and remove .,-()
                word = word.lower()
                char_excl = [".", ",", "-", "(", ")"]
                for c in char_excl:
                    word = word.replace(c, "")
                # not part of a formula environment
                not_formula = not True in [ex in word for ex in excluded]
                # not stopword
                not_stopword = word not in stopwords
                if not_formula and not_stopword:
                    # count occurences
                    try:
                        matches[word] += 1
                    except:
                        matches[word] = 1

        annotation_candidates[identifier[0]] = OrderedDict(sorted(matches.items(), key=itemgetter(1), reverse=True))

        f = open(mypath + "\\output2\\" + "annotation_candidates.pkl", "wb")
        pickle.dump(OrderedDict(sorted(annotation_candidates.items())), f)
        f.close()

print("end")