import os
import urllib3
import json
import re
import logging
urllib3.disable_warnings()
from github import Github, GithubException
from .formula_concept_handler import FormulaConceptHandler

logging.basicConfig(level=logging.WARNING)
data_repo_handler_logger = logging.getLogger(__name__)

class DataRepoHandler:
    """
    Handles everything that needs to access the data repo ag-gipp/dataAnnoMathTex.
    """

    def __init__(self, token=os.getenv('apikey', False)):
        self.token = token

        if not token:
            try:
                from ...views.helper_classes.key import local_token
                self.token = local_token
            except Exception:
                data_repo_handler_logger.info('Token not set')


        if not self.token:
            data_repo_handler_logger.info('Token not set')
            exit(2)


        self.g = Github(self.token)
        self.repo = self.g.get_repo("ag-gipp/dataAnnoMathTeX")
        self.user = self.g.get_user()
        self.evaluation_folder = 'evaluation'

    def commit_file(self, file_name, file_content):
        #return
        try:
            self.repo.create_file(file_name, "commiting file {}".format(file_name), file_content)
        except GithubException as e:
            #data_repo_handler_logger.info(e)
            contents = self.repo.get_contents(file_name)
            self.repo.update_file(file_name, "updating file {}".format(file_name), file_content, contents.sha)
            #data_repo_handler_logger.info("updating file {}".format(file_name))
        except AttributeError as e:
            pass
            #data_repo_handler_logger.info(e)

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
        #try:
        #    self.delete_file(path)
        #    data_repo_handler_logger.info('Deleting annotation file')
        #except Exception as e:
        #    data_repo_handler_logger.info('No previous annotation file')
        #data_repo_handler_logger.info('annotations: ')
        #data_repo_handler_logger.info(annotations)
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

    def get_wikidata_identifiers_by_name(self):
        encoded_content = self.repo.get_file_contents('sources/wikidata_identifiers_by_name.json')
        decoded_content = encoded_content.decoded_content
        identifiers = json.loads(decoded_content.decode("utf-8"))
        return identifiers

    def get_wikidata_formulae(self):
        encoded_content = self.repo.get_file_contents('sources/wikidata_formulae.json')
        decoded_content = encoded_content.decoded_content
        formulae = json.loads(decoded_content.decode("utf-8"))
        return formulae

    def get_math_wikidata_items(self):
        encoded_content = self.repo.get_file_contents('sources/math_wikidata_items.json')
        decoded_content = encoded_content.decoded_content
        items = json.loads(decoded_content.decode("utf-8"))
        return items

    def list_directory(self, dirname='files'):
        dir_contents = self.repo.get_dir_contents(dirname)
        def clean_name(content_file):
            #regex = r'(?<={}/).*?(?=\.(txt|tex))'.format(dirname)
            regex = r'(?<={}/).*?\.(txt|tex)'.format(dirname)
            file_name = re.search(regex, str(content_file))
            file_name = file_name.group()
            file_name = file_name.replace('_', ' ')
            if ('.txt' in file_name):
                file_name = file_name.replace('.txt', ' (Wikitext)')
            else:
                file_name = file_name.replace('.tex', ' (LaTeX)')
            return file_name

        file_names = list(map(clean_name, dir_contents))
        return file_names

    def get_wikipedia_article(self, article_name):
        article_name = article_name.replace(' (Wikitext)', '.txt')
        article_name = article_name.replace(' (LaTeX)', '.tex')
        article_name = article_name.replace(' ', '_')
        path = 'files/{}'.format(article_name)
        encoded_content = self.repo.get_file_contents(path)
        decoded_content = encoded_content.decoded_content
        return decoded_content

    def get_annotation_file(self, article_name):


        #if article_name + ' annotation ' in self.list_directory(dirname='annotation'):
        if article_name in self.list_directory(dirname='annotation'):
            article_name = article_name.replace(' (Wikitext)', '.txt')
            article_name = article_name.replace(' (LaTeX)', '.tex')
            article_name = article_name.replace(' ', '_')


            #annotation_file_name = article_name.replace(' ', '_')
            #annotation_file_name = '{}_annotation_.txt'.format(annotation_file_name)
            #annotation_file_name = '{}.txt'.format(article_name)
            path = 'annotation/{}'.format(article_name)

            data_repo_handler_logger.info(path)

            encoded_content = self.repo.get_file_contents(path)
            decoded_content = encoded_content.decoded_content
            decoded_content_str = decoded_content.decode()
            return decoded_content_str


    def add_wikipedia_article_to_repo(self, article, article_name):
        path = 'files/{}.txt'.format(article_name.replace(' ', '_'))
        self.commit_file(path, article)
        return

    def formula_concept_db_first_commit(self, formulae):
        self.commit_file('sources/formula_concepts.txt', formulae)


class ManualRecommendationsCleaner:
    """
    Prepares the manual recommendations for adding them to the manual recommendations file.
    """

    def __init__(self, manual_recommendations):
        self.manual_recommendations = manual_recommendations

    def get_recommendations(self):
        cleaned_manual_recommendations = []


        data_repo_handler_logger.info(self.manual_recommendations)

        for id_or_f in self.manual_recommendations:
                for d in self.manual_recommendations[id_or_f]:
                    data_repo_handler_logger.info(self.manual_recommendations[id_or_f])
                    try:
                        name = d['name']
                        id_or_f = id_or_f.replace('__EQUALS__', '=')
                        cleaned_manual_recommendations.append((id_or_f, name))
                    except Exception as e:
                        #item = self.manual_recommendations[id_or_f][num]
                        msg = 'could not add to manual recommendations '# + num
                        data_repo_handler_logger.info(msg)
                        data_repo_handler_logger.info(self.manual_recommendations[id_or_f])

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
    drh = DataRepoHandler(local_token)
    dir = drh.list_directory()
    annotation_files = filter(lambda f: 'annotation' not in f, dir)
    for fn in annotation_files:
        original_fn = fn + '.txt'
        #new_fn = original_fn.replace('__', '_')
        old_path = 'annotation/{}'.format(original_fn)
        new_path = 'files/{}'.format(original_fn)
        drh.rename_file(old_file_name=old_path, new_file_name=new_path)


def wikidata_identifiers_by_name_old(d):
    identifiers = d.get_wikidata_identifiers()

    def f(i):
        symbol = i[0]
        if i[1]:
            name = i[1][0]['name']
            del i[1][0]['name']
            i[1][0]['symbol'] = symbol
            return (name, i[1])

        return i

    identifiers_by_name = dict(filter(lambda i: len(i[1]) > 0, map(f, identifiers.items())))
    d.commit_file('sources/wikidata_identifiers_by_name.json', json.dumps(identifiers_by_name))



def wikidata_identifiers_by_name(d):
    identifiers = d.get_wikidata_identifiers()

    identifiers_by_name = {}
    for symbol in identifiers:
        for item in identifiers[symbol]:
            name = item['name']
            del item['name']
            item['symbol'] = symbol
            identifiers_by_name[name] = item


    d.commit_file('sources/wikidata_identifiers_by_name.json', json.dumps(identifiers_by_name))


def commit_all_wikidata_items():
    path = '/volumes/Stuff/all.json'

    with open(path) as infile:
        print(infile.read()[:100])
        data = json.load(infile)
        print(data['Douglas Adams'])

def commit_wikidata_math_items(d):
    path = '/Users/ianmackerracher/PycharmProjects/AnnoMathTeX/files/math_wikidata_items.json'

    items = {}

    with open(path) as infile:
        data = json.load(infile)
        for item in data:
            try:
                qid = re.search(r'(?<=/entity/)[Q|P][0-9]+'  ,item['item']).group()
                name = item['itemLabel']
                items[name] = qid
            except Exception:
                print(item)

        d.commit_file('sources/math_wikidata_items.json', json.dumps(items))



def merge_math_files(d):
    math_wikidata_items = d.get_math_wikidata_items()
    wikidata_identifiers = d.get_wikidata_identifiers()


    for value in wikidata_identifiers.values():
        for item in value:
            qid = item['qid']
            if qid not in math_wikidata_items.values():
                name = item['name']
                math_wikidata_items[name] = qid


    d.delete_file('sources/math_wikidata_items.json')
    d.commit_file('sources/math_wikidata_items.json', json.dumps(math_wikidata_items))





if __name__ == '__main__':
    #For testing purposes
    from key import local_token

    import os
    d = DataRepoHandler(local_token)
    #a = d.get_wikipedia_article('Angular velocity')
    #decode_wikipedia_article(a)
    #d.delete_file('files/Sphere.txt')
    #d.delete_file('evaluation/Astronomical_spectroscopy.txt.csv')
    #wikidata_identifiers_by_name(d)

    #commit_all_wikidata_items()
    #commit_wikidata_math_items(d)
    merge_math_files(d)
