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

# annotation_catalog = {}
with open(mypath + "\\output2\\" + "annotation_catalog_all.pkl", "rb") as f:
    annotation_catalog = pickle.load(f)

annotation_candidates = {}
# with open(mypath + "\\output2\\" + "annotation_candidates.pkl", "rb") as f:
#     annotation_candidates = pickle.load(f)

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

        f = open(mypath + "\\output2\\" + "annotation_candidates_all.pkl", "wb")
        pickle.dump(OrderedDict(sorted(annotation_candidates.items())), f)
        f.close()