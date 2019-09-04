import os
import urllib3
import json
import re
urllib3.disable_warnings()
from github import Github, GithubException



class DataRepoHandler:
    """
    Handles everything that needs to access the data repo ag-gipp/dataAnnoMathTex.
    """

    def __init__(self, token=os.getenv('apikey', False)):
        self.token = token

        if not token:
            print('token: ', token)
            try:
                from .key import local_token
                self.token = local_token
            except Exception:
                print('Token not set')


        if not self.token:
            print('Token not set')
            exit(2)


        self.g = Github(self.token)
        self.repo = self.g.get_repo("ag-gipp/dataAnnoMathTex")
        self.user = self.g.get_user()
        self.evaluation_folder = 'evaluation'

    def commit_file(self, file_name, file_content):
        #return
        try:
            self.repo.create_file(file_name, "commiting file {}".format(file_name), file_content)
        except GithubException as e:
            print(e)
            contents = self.repo.get_contents(file_name)
            self.repo.update_file(file_name, "updating file {}".format(file_name), file_content, contents.sha)
            print("updating file {}".format(file_name))
            print(file_content)
        except AttributeError as e:
            print(e)
        return

    def delete_file(self, file_name):
        contents = self.repo.get_contents(file_name)
        self.repo.delete_file(file_name, "Deleting file {}".format(file_name), contents.sha)
        return

    def rename_file(self, old_file_name, new_file_name):
        encoded_content = self.repo.get_file_contents(old_file_name)
        decoded_content = encoded_content.decoded_content
        self.delete_file(old_file_name)
        self.commit_file(new_file_name, decoded_content)
        return

    def commit_formula_concepts(self, annotations):
        f = FormulaConceptHandler(annotations)
        formulae = f.get_formulae()
        encoded_content = self.repo.get_file_contents('sources/formula_concepts.txt')
        decoded_content = encoded_content.decoded_content
        formula_concepts = json.loads(decoded_content)

        for new_formula_name in formulae:
            if new_formula_name in formula_concepts:
                new_formula_tex_string = formulae[new_formula_name]['TeXStrings'][0]
                if new_formula_tex_string not in formula_concepts[new_formula_name]['TeXStrings']:
                    formula_concepts[new_formula_name]['TeXStrings'].append(new_formula_tex_string)

            else:
                formula_concepts[new_formula_name] = formulae[new_formula_name]

        self.commit_file('sources/formula_concepts.txt', json.dumps(formula_concepts))
        return

    def tmp(self):
        encoded_content = self.repo.get_file_contents('sources/formula_concepts.txt')
        decoded_content = encoded_content.decoded_content
        formula_concepts = json.loads(decoded_content)

        del formula_concepts['dummy_formula']

        self.commit_file('sources/formula_concepts.txt', json.dumps(formula_concepts))



    def commit_manual_recommendations(self, cleaned_manual_recommendations):
        encoded_content = self.repo.get_file_contents('sources/manual_recommendations.txt')
        decoded_content = encoded_content.decoded_content
        existing_manual_recommendations = json.loads(decoded_content)

        for id_or_f, name in cleaned_manual_recommendations:

            if id_or_f in existing_manual_recommendations:
                for item in existing_manual_recommendations[id_or_f]:
                    if name == item['name']:
                        item['count'] += 1
                        break
            else:
                existing_manual_recommendations[id_or_f] = [{'name': name,
                                                             'count': 1}]

        self.commit_file('sources/manual_recommendations.txt', json.dumps(existing_manual_recommendations))
        return

    def get_manual_recommendations(self):
        encoded_content = self.repo.get_file_contents('sources/manual_recommendations.txt')
        decoded_content = encoded_content.decoded_content
        existing_manual_recommendations = json.loads(decoded_content)
        return existing_manual_recommendations

    def get_formula_concepts(self):
        encoded_content = self.repo.get_file_contents('sources/formula_concepts.txt')
        decoded_content = encoded_content.decoded_content
        formula_concepts = json.loads(decoded_content)
        return formula_concepts

    def commit_annotations(self, annotations_file_name, annotations):
        path = 'annotation/{}'.format(annotations_file_name)
        self.commit_file(path, annotations)
        return

    def commit_evaluation(self, evaluation_file_name, evaluation_csv_string):
        path = 'evaluation/{}'.format(evaluation_file_name)
        self.commit_file(path, evaluation_csv_string)
        return


    def commit_to_repo(self, csv_file_name, csv_file_content, annotations):
        self.commit_file(csv_file_name, csv_file_content)
        self.commit_formula_concepts(annotations)
        return

    def get_wikidata_identifiers(self):
        encoded_content = self.repo.get_file_contents('sources/wikidata_identifiers.json')
        decoded_content = encoded_content.decoded_content
        identifiers = json.loads(decoded_content.decode("utf-8"))
        return identifiers

    def get_wikidata_formulae(self):
        encoded_content = self.repo.get_file_contents('sources/wikidata_formulae.json')
        decoded_content = encoded_content.decoded_content
        formulae = json.loads(decoded_content.decode("utf-8"))
        return formulae

    def list_directory(self, dirname='files'):
        dir_contents = self.repo.get_dir_contents(dirname)
        print(dir_contents)
        def clean_name(content_file):
            regex = r'(?<={}/).*?(?=\.txt)'.format(dirname)
            file_name = re.search(regex, str(content_file))
            file_name = file_name.group()#[0]
            file_name = file_name.replace('_', ' ')
            return file_name

        file_names = list(map(clean_name, dir_contents))
        return file_names

    def get_wikipedia_article(self, article_name):
        article_name = article_name.replace(' ', '_')
        path = 'files/{}.txt'.format(article_name)
        encoded_content = self.repo.get_file_contents(path)
        decoded_content = encoded_content.decoded_content
        return decoded_content

    def get_annotation_file(self, article_name):

        #annotation_directory = self.list_directory('annotation')
        #for a in annotation_directory:
        #    print(a, article_name, a == article_name + ' annotation ')

        if article_name + ' annotation ' in self.list_directory('annotation'):
            annotation_file_name = article_name.replace(' ', '_')
            annotation_file_name = '{}_annotation_.txt'.format(annotation_file_name)
            path = 'annotation/{}'.format(annotation_file_name)
            encoded_content = self.repo.get_file_contents(path)
            decoded_content = encoded_content.decoded_content
            decoded_content_str = decoded_content.decode()
            return decoded_content_str


    def add_wikipedia_article_to_repo(self, article, article_name):
        path = 'files/{}.txt'.format(article_name.replace(' ', '_'))
        self.commit_file(path, article)
        return




class FormulaConceptHandler:
    """
    Prepares the formulae for adding to the formula concepts file.
    """

    def __init__(self, annotations):
        self.annotations = annotations

    def extract_formulae(self):
        formulae = {}


        print('FORMULA CONCEPT HANDLER:\n')
        print(self.annotations)

        if 'global' in self.annotations:
            g = self.annotations['global']
            for key in g:
                instance = g[key]
                if instance['type'] == 'Formula':
                    #print(instance)
                    formulae[key.replace('__EQUALS__', '=')] = {
                        'name': instance['name'].replace('__EQUALS__', '=')
                        #'sourcesWithNums': instance['sourcesWithNums']
                    }

        if 'local' in self.annotations:
            l = self.annotations['local']
            for key in l:
                for unique_id in l[key]:
                    instance = l[key][unique_id]
                    if instance['type'] == 'Formula':
                        formulae[key.replace('__EQUALS__', '=')] = {
                            'name': instance['name'].replace('__EQUALS__', '=')
                            #'sourcesWithNums': instance['sourcesWithNums']
                        }

        return formulae


    def add_identifiers(self):
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



class ManualRecommendationsCleaner:
    """
    Prepares the manual recommendations for adding them to the manual recommendations file.
    """

    def __init__(self, manual_recommendations):
        self.manual_recommendations = manual_recommendations

    def get_recommendations(self):
        cleaned_manual_recommendations = []

        for id_or_f in self.manual_recommendations:
                for num in self.manual_recommendations[id_or_f]:
                    name = self.manual_recommendations[id_or_f][num]['name']
                    id_or_f = id_or_f.replace('__EQUALS__', '=')
                    cleaned_manual_recommendations.append((id_or_f, name))

        return cleaned_manual_recommendations



def read_evaluation_file_json(file_name):
    with open(os.getcwd() + '/evaluation_files/' + file_name) as infile:
        file_json = json.load(infile)
    return file_json


def decode_wikipedia_article(wikipedia_article):
    print(type(wikipedia_article))
    wikipedia_article = wikipedia_article.decode()
    print(type(wikipedia_article))
    print(wikipedia_article)



def move_files_to_file_folder():
    from key import local_token
    import os
    drh = DataRepoHandler(local_token)
    dir = drh.list_directory()
    annotation_files = filter(lambda f: 'annotation' not in f, dir)
    for fn in annotation_files:
        original_fn = fn + '.txt'
        #new_fn = original_fn.replace('__', '_')
        old_path = 'annotation/{}'.format(original_fn)
        new_path = 'files/{}'.format(original_fn)
        drh.rename_file(old_file_name=old_path, new_file_name=new_path)



if __name__ == '__main__':
    #For testing purposes
    from key import local_token
    import os
    d = DataRepoHandler(local_token)
    #a = d.get_wikipedia_article('Angular velocity')
    #decode_wikipedia_article(a)

    d.delete_file('files/Test.txt')



