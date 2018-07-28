from read_doc import read_doc
from extract_formulae import extract_formulae
from process_formulae import process_formulae
from process_json import create_json, load_json, save_json

#read in document and extract formulae
doc = read_doc()
formulae = extract_formulae(doc)

#load formulae from json file or create a new dictionary
formulae_path = 'formulae.json'
try:
    formulae_json = load_json(formulae_path)
except:
    formulae_json = create_json()

#parse formulae and fetch annotation from user input
formulae_json = process_formulae(formulae, formulae_json)

# # print json content
# for formula in formulae_json.Formulae:
#     for identifier in formula.Identifiers:
#         print(identifier.Name)

# #formula annotation recommendation
# for formula_iter in formulae_json.Formulae:
#     print(formula_iter.Expression==formulae[0])

#save formulae and identifiers in json file
save_json(formulae_json, formulae_path)