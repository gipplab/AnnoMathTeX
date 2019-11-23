import os
import re
from .settings.common import PROJECT_ROOT

#Limit of the number of recommendations that are returned
recommendations_limit = 10
arxiv_evaluation_file_path = os.path.join(PROJECT_ROOT, 'annomathtex', 'recommendation', 'evaluation_files', 'Evaluation_list_all.rtf')
wikipedia_evaluation_file_path = os.path.join(PROJECT_ROOT, 'annomathtex', 'recommendation', 'evaluation_files', 'wikipedia_list.json')

#evaluation_annotations_path = os.getcwd() + '/../evaluation/annotations/'
evaluation_annotations_path = os.path.join(os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir)), 'evaluation', 'annotations')

#project_root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
#evaluation_annotations_path = os.path.join(project_root, ['evaluation', 'annotations'])

def create_annotation_file_name(file_name):
    file_name = file_name.replace(' (Wikitext)', '')
    file_name = file_name.replace(' (LaTeX)', '')
    annotation_file_name = re.sub(r'\s', '_', file_name) + '.txt'
    return annotation_file_name


def create_file_name(file_name):
    extension = '.txt' if '(Wikitext)' in file_name else '.tex'
    file_name = file_name.replace(' (Wikitext)', '')
    file_name = file_name.replace(' (LaTeX)', '')
    file_name = re.sub(r'\s', '_', file_name) #+ extension
    file_name_with_extension = re.sub(r'\s', '_', file_name) + extension
    return file_name, file_name_with_extension

def create_annotation_file_path(file_name):
    return os.path.join(evaluation_annotations_path, create_annotation_file_name(file_name))


def create_evaluation_file_name(file_name):
    evaluation_file_name = re.sub(r'\..*', '.csv', file_name)
    #file_name = file_name.replace('.txt', '')
    #file_name = file_name.replace('.tex', '')
    #file_name = file_name.replace('.html', '')
    evaluation_file_name = re.sub(r'\s', '_', file_name) + '.csv'
    return evaluation_file_name

def create_evaluation_file_path(file_name):
    return os.path.join(evaluation_annotations_path, create_evaluation_file_name(file_name))

#evaluations_path = evaluation_annotations_path + 'evaluation_file.csv'


#view_cache_path = os.getcwd() + '/annomathtex/views/cache/'
view_cache_path = os.path.join(PROJECT_ROOT, 'annomathtex', 'views', 'cache')

file_name_cache_path = os.path.join(os.getcwd(), 'annomathtex', 'views', 'cache', 'file_name_cache.txt')

file_name_cache_path_deployed_sys = os.path.join(os.getcwd(), 'annomathtex', 'annomathtex', 'views', 'cache', 'file_name_cache.txt')
