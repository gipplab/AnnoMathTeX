import os
import urllib3
import json
urllib3.disable_warnings()
from github import Github, GithubException



class DataRepoHandler:

    def __init__(self, token=os.getenv('apikey', False)):
        self.token = token

        #uncomment for local testing
        #if not token:
        #    from .key import local_token
        #    self.token = local_token

        #uncomment for wmflabs
        if not token:
            print('Token not set')
            exit(2)


        self.g = Github(self.token)
        self.repo = self.g.get_repo("ag-gipp/dataAnnoMathTex")
        self.user = self.g.get_user()

    def commit_file(self, file_name, file_content):
        print('committing file {}'.format(file_name))
        try:
            self.repo.create_file(file_name, "commiting file {}".format(file_name), file_content)
        except GithubException as e:
            print(e)
            contents = self.repo.get_contents(file_name)
            self.repo.update_file(file_name, "updating file {}".format(file_name), file_content, contents.sha)
        except AttributeError as e:
            print(e)
        return

    def delete_file(self, file_name):
        contents = self.repo.get_contents(file_name)
        self.repo.delete_file(file_name, "Deleting file {}".format(file_name), contents.sha)
        return

    def commit_formula_concepts(self, annotations):
        f = FormulaConceptHandler(annotations)
        formulae = f.get_formulae()
        encoded_content = self.repo.get_file_contents('formula_concepts.txt')
        decoded_content = encoded_content.decoded_content
        formula_concepts = json.loads(decoded_content)

        for new_formula_name in formulae:
            if new_formula_name in formula_concepts:
                new_formula_tex_string = formulae[new_formula_name]['TeXStrings'][0]
                if new_formula_tex_string not in formula_concepts[new_formula_name]['TeXStrings']:
                    formula_concepts[new_formula_name]['TeXStrings'].append(new_formula_tex_string)

            else:
                formula_concepts[new_formula_name] = formulae[new_formula_name]

        self.commit_file('formula_concepts.txt', json.dumps(formula_concepts))
        return


    def commit_to_repo(self, csv_file_name, csv_file_content, annotations):
        self.commit_file(csv_file_name, csv_file_content)
        self.commit_formula_concepts(annotations)
        return




class FormulaConceptHandler:

    #todo: simplify

    def __init__(self, annotations):
        self.annotations = annotations

    def extract_formulae(self):
        formulae = {}

        if 'global' in self.annotations:
            g = self.annotations['global']
            for key in g:
                instance = g[key]
                if instance['type'] == 'Formula':
                    #print(instance)
                    formulae[key] = {
                        'name': instance['name']
                        #'sourcesWithNums': instance['sourcesWithNums']
                    }

        if 'local' in self.annotations:
            l = self.annotations['local']
            for key in l:
                for unique_id in l[key]:
                    instance = l[key][unique_id]
                    if instance['type'] == 'Formula':
                        formulae[key] = {
                            'name': instance['name']
                            #'sourcesWithNums': instance['sourcesWithNums']
                        }



        return formulae


    def add_identifiers(self):

        #print('FORMULA HANDLE')

        formulae = self.extract_formulae()

        if 'global' in self.annotations:
            g = self.annotations['global']
            for key in g:
                instance = g[key]
                m = instance['mathEnv']
                is_identifier = True if instance['type'] == 'Identifier' else False
                if m in formulae and is_identifier:
                    if 'identifiers' in formulae[m]:
                        formulae[m]['identifiers'][key] = instance['name']
                    else:
                        formulae[m]['identifiers'] = {key: instance['name']}

        if 'local' in self.annotations:
            l = self.annotations['local']
            for key in l:
                for unique_id in l[key]:
                    instance = l[key][unique_id]
                    m = instance['mathEnv']
                    is_identifier = True if instance['type'] == 'Identifier' else False
                    if m in formulae and is_identifier:
                        if 'identifiers' in formulae[m]:
                            formulae[m]['identifiers'][key] = instance['name']
                        else:
                            formulae[m]['identifiers'] = {key: instance['name']}


        return formulae


    def get_formulae(self):
        formulae = self.add_identifiers()
        reversed_formulae = {}

        for formula_string in formulae:
            name = formulae[formula_string]['name']
            identifiers = formulae[formula_string]['identifiers']
            reversed_formulae[name] = {'TeXStrings': [formula_string],
                                       'Identifiers': identifiers}



        return reversed_formulae









if __name__ == '__main__':
    from key import local_token
    d = DataRepoHandler(local_token)
    #d.delete_file('formula_concepts.txt')
    #initial_formulae_file = json.dumps({'dummy_formula': {'TeXStrings': ['empty'], 'Identifiers': 'empty'}})
    initial_formulae_file = json.dumps({})
    d.commit_file('formula_concepts.txt', initial_formulae_file)






