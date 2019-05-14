import os
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
    file_name = file_name.replace('.txt', '')
    file_name = file_name.replace('.tex', '')
    file_name = file_name.replace('.html', '')
    annotation_file_name = file_name + '__annotation__.txt'
    return annotation_file_name


def create_annotation_file_path(file_name):
    return os.path.join(evaluation_annotations_path, create_annotation_file_name(file_name))


def create_evaluation_file_name(file_name):
    file_name = file_name.replace('.txt', '')
    file_name = file_name.replace('.tex', '')
    file_name = file_name.replace('.html', '')
    evaluation_file_name = file_name + '__evaluation__.csv'
    return evaluation_file_name

def create_evaluation_file_path(file_name):
    return os.path.join(evaluation_annotations_path, create_evaluation_file_name(file_name))

#evaluations_path = evaluation_annotations_path + 'evaluation_file.csv'


#view_cache_path = os.getcwd() + '/annomathtex/views/cache/'
view_cache_path = os.path.join(PROJECT_ROOT, 'annomathtex', 'views', 'cache')
