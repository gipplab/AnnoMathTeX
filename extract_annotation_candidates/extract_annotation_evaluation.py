import pickle

#global path
mypath = "F:\\arXiv"

with open(mypath + "\\output2\\" + "annotation_candidates.pkl", "rb") as f:
    annotation_candidates = pickle.load(f)

Evaluation_list = []

for identifier in annotation_candidates.items():
    Evaluation_list.append(identifier[0])
    candidates = list(identifier[1])
    # top 10 candidates
    for candidate in candidates[:10]:
        Evaluation_list.append(candidate + ": " + str(annotation_candidates[identifier[0]][candidate]))
    Evaluation_list.append("")

import codecs

with codecs.open("output\\Evaluation_list.txt", "w", "utf-8") as f:
    f.write("\n".join(Evaluation_list))

print("end")