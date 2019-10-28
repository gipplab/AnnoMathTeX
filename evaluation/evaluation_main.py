from evaluation_dr_handler import EvaluationDRHandler
from io import StringIO
import csv




def eval_files_as_one():
    eval_file_ignore_list = ['one_eval_file.csv']
    all_eval_files = EvaluationDRHandler().get_all_evaluation_files(eval_file_ignore_list)
    header = all_eval_files[0][0]
    def check_empty(file):
        if len(file) == 0:
            return True
        if len(file[0]) == 0:
            return True
        return False

    eval_files = [file[1:] for file in all_eval_files if not check_empty(file[1:])]
    flatten = lambda all: [item for file in all for item in file if len(item)>0]
    one_eval_file = flatten(eval_files)

    return [header] + one_eval_file


def commit_one_eval_file():
    f = StringIO()
    eval_file = eval_files_as_one()
    csv.writer(f).writerows(eval_file)
    csv_string =  f.getvalue()

    dr_handler = EvaluationDRHandler()
    file_name = 'evaluation/one_eval_file.csv'
    dr_handler.delete_file(file_name)
    dr_handler.commit_file(file_name, csv_string)


def get_one_evaluation_file():
    return EvaluationDRHandler().get_file('evaluation/one_eval_file.csv')


def split_formulae_identifiers(eval_file):
    #return formulae_rows, identifier_rows
    pass

def selection_ranking_sources(eval_file):
    pass

def local_vs_global(eval_file):
    pass

def average_selection_time(eval_file):
    pass

def average_manual_time(eval_file):
    pass

def proportion_qid_available(eval_file):
    pass

def time_saved_through_global(annotation_file):
    pass



if __name__ == '__main__':
    #commit_one_eval_file()

    print(get_one_evaluation_file())