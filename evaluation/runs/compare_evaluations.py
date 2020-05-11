import os

# OPEN FILES
mode = "evaluation"
root = "C:\\Users/Philipp/Dropbox/PhD/Projects/Annotation Recommender/dataAnnoMathTex/runs"

articles = ['Astronomical_spectroscopy.csv', 'Compton_scattering.csv', 'Critical_ionization_velocity.csv', 'Darwin–Radau_equation.csv', 'Dynamical_friction.csv', 'Epicyclic_frequency.csv', 'Forbidden_mechanism.csv', 'M–sigma_relation.csv', 'Planck_length.csv']
#article = "Astronomical_spectroscopy"
article = articles[8]
annotators = ["Ian","Philipp(keepFCDB)"]

files = []

# for file in os.listdir(root + "/" + annotators[0] + "/" + mode):
#     files.append(file)

for annotator in annotators:
    #files.append(article + "_" + mode + "_" + annotator + ending)
    files.append(root + "/" + annotator + "/" + mode + "/" + article)

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

# output if annotations are different (for Annotation Guide)
difference_lines = []
for expression in expression_annotations.items():
    try:
        if expression[1][0] != expression[1][1]:
            difference_lines.append("'" + expression[0] + "'" + ";" +
                                    "['" + expression[1][0] + "', '" +
                                    expression[1][1] + "']" + "\n")
    except:
        # only one annotation available
        pass

with open("difference_lines'.csv",'w') as f:
    f.writelines(difference_lines)

print("end")