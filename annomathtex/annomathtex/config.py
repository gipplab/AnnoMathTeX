import os

#Limit of the number of recommendations that are returned
recommendations_limit = 10

arxiv_evaluation_file_path = os.getcwd() + '/annomathtex/recommendation/evaluation_files/Evaluation_list_all.rtf'
wikipedia_evaluation_file_path = os.getcwd() + '/annomathtex/recommendation/evaluation_files/wikipedia_list.json'

evaluation_annotations_path = os.getcwd() + '/../evaluation/annotations/'
#project_root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
#evaluation_annotations_path = os.path.join(project_root, ['evaluation', 'annotations'])

def create_annotation_file_name(file_name):
    annotation_file_name = file_name.replace('.', '__DOT__') + '__ANN__.txt'
    #return os.path.join(evaluation_annotations_path, annotation_file_name)

    return annotation_file_name


def create_annotation_file_path(file_name):
    return evaluation_annotations_path + create_annotation_file_name(file_name)


evaluations_path = evaluation_annotations_path + 'evaluation_file.csv'


view_cache_path = os.getcwd() + '/annomathtex/views/cache/'
