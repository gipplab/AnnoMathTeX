# OPEN FILES
mode = "evaluation"
root = "C:\\Users/Philipp/Dropbox/PhD/Projects/Annotation Recommender/dataAnnoMathTex/runs"

article = "Astronomical_spectroscopy"
annotators = ["Ian","Philipp(keepFCDB)"]

files = []

for annotator in annotators:
   files.append(root + "/" + annotator + "/" + mode + "/" + article + ".csv")

contents = []
for file in files:
    with open(file) as f:
        contents.append(f.readlines())

# DEFINE FUNCTIONS
def add_element_to_dict_list(dict,list,element):
    try:
        dict[list].append(element)
    except:
        dict[list] = []
        dict[list].append(element)

# CREATE ANNOTATIONS COMPARISON DICT
expression_annotations = {}
for content in contents:
    for line in content:
        if not line.startswith("Identifier"):
            parts = line.split(",")
            expression_string = parts[0]
            expression_annotation = parts[1]
            add_element_to_dict_list(expression_annotations,
                                     expression_string,expression_annotation)

# OPEN WIKITEXT
wikitext_path = root + "/files/" + article + ".txt"
with open(wikitext_path,"r",encoding='utf-8') as f:
    wikitext_text = f.read()

formulae_in_math_env = {}
for expression in expression_annotations.keys():
    if expression in wikitext_text:
        position = wikitext_text.find(">" + expression + "<")
        math_tag = wikitext_text[position-10:position+10]
        if len(math_tag) > 0:
            formulae_in_math_env[expression] = expression_annotations[expression]
        expression_annotations[expression].append(math_tag)

print("end")