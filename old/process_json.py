from old.JsonConvert import JsonConvert, Formulae


def create_json():

    # create dictionary for formulae
    formulae_json = Formulae()

    return formulae_json

def load_json(formulae_path):

    # load formulae from json file
    formulae_json = JsonConvert.FromFile(formulae_path)

    return formulae_json

def save_json(formulae_json, formulae_path):

    # save formulae in json file
    JsonConvert.ToFile(formulae_json, formulae_path)