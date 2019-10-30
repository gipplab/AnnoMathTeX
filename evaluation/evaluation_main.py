from evaluation_dr_handler import EvaluationDRHandler
from functools import reduce
from io import StringIO
import csv
import string
import re



def list_to_csv(list):
    f = StringIO()
    csv.writer(f).writerows(list)
    csv_string =  f.getvalue()
    return csv_string



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
    #f = StringIO()
    #eval_file = eval_files_as_one()
    #csv.writer(f).writerows(eval_file)
    #csv_string =  f.getvalue()

    csv_string = list_to_csv(eval_files_as_one())

    dr_handler = EvaluationDRHandler()
    file_name = 'evaluation/one_eval_file.csv'
    dr_handler.delete_file(file_name)
    dr_handler.commit_file(file_name, csv_string)


def get_one_evaluation_file():
    eval_file_string = EvaluationDRHandler().get_file('evaluation/one_eval_file.csv')
    eval_file_list = eval_file_string.split('\r\n')
    eval_file = [r.split(',') for r in eval_file_list]
    eval_file = list(filter(lambda r: len(r[0])>0, eval_file))
    return eval_file


def split_formulae_identifiers(eval_file):
    formulae = []
    identifiers = []

    header = [eval_file[0]]

    for row in eval_file[1:]:
        overlap = list(set(row[0]) & set(string.punctuation))
        if overlap:
            formulae.append(row)
        else:
            identifiers.append(row)
    return header + formulae, header + identifiers


def get_rank(num, eval_file):

    def f(r):
        if r[num] != '-':
            return r[num]
    return list(filter(lambda x: x ,map(f, eval_file[1:])))


def selection_ranking_sources_formulae(eval_file):

    wikidata1 = get_rank(5, eval_file)
    wikidata2 = get_rank(6, eval_file)
    word_window = get_rank(7, eval_file)
    fcdb = get_rank(8, eval_file)
    #manual = []


    def create_csv_file():
        header = ['source', 'total', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        def count(source, num):
            return len(list(filter(lambda x: x==str(num), source)))
        wikidata1_row = ['Wikidata1', len(wikidata1)] + [count(wikidata1, num) for num in range(1,11)]
        wikidata2_row = ['Wikidata2', len(wikidata2)] + [count(wikidata2, num) for num in range(1,11)]
        word_window_row = ['WordWindow', len(word_window)] + [count(word_window, num) for num in range(1, 11)]
        fcdb_row = ['FCDB', len(fcdb)] + [count(fcdb, num) for num in range(1,11)]


        all = [header] + [wikidata1_row] + [wikidata2_row] + [word_window_row] + [fcdb_row]
        csv_string = list_to_csv(all)
        return csv_string

    return create_csv_file()


def selection_rankging_sources_identifiers(eval_file):



    arxiv = get_rank(2, eval_file)
    wikipedia = get_rank(3, eval_file)
    wikidata = get_rank(4, eval_file)
    word_window = get_rank(7, eval_file)
    #manual = []


    def create_csv_file():
        header = ['source', 'total', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        def count(source, num):
            return len(list(filter(lambda x: x==str(num), source)))
        arxiv_row = ['arXiv', len(arxiv)] + [count(arxiv, num) for num in range(1,11)]
        wikipedia_row = ['Wikipedia', len(wikipedia)] + [count(wikipedia, num) for num in range(1,11)]
        wikidata_row = ['Wikidata', len(wikidata)] + [count(wikidata, num) for num in range(1,11)]
        word_window_row = ['WordWindow', len(word_window)] + [count(word_window, num) for num in range(1,11)]

        all = [header] + [arxiv_row] + [wikipedia_row] + [wikidata_row] + [word_window_row]
        csv_string = list_to_csv(all)
        return csv_string


    return create_csv_file()


def local_vs_global(eval_file):
    """
    Number of global and local annotations
    :param eval_file:
    :return:
    """

    g = len(list(filter(lambda x: x[9] == 'global', eval_file[1:])))
    l = len(eval_file[1:]) - g

    return {'global':g, 'local':l}


def average_selection_time(eval_file):
    #column_num = -2
    selection_times = [int(r[-2]) for r in eval_file[1:] if int(r[-1]) == -1]
    avg_selection_time = sum(selection_times) / len(selection_times)

    return round(avg_selection_time)


def average_manual_time(eval_file):
    selection_times = [int(r[-1]) for r in eval_file[1:] if int(r[-1]) > -1]
    avg_selection_time = sum(selection_times) / len(selection_times)

    return {'avg': round(avg_selection_time), 'total num': len(selection_times)}


def proportion_qid_available(eval_file):

    names = [r[1] for r in eval_file[1:]]
    have_qid = list(filter(lambda x: re.search(r'(?<=\()Q[0-9]+(?=\))', x), names))
    qid_num = len(have_qid)
    no_qid_num = len(names) - qid_num

    return {'have qid': qid_num, 'no qid': no_qid_num}



def time_saved_through_global():
    annotation_files = EvaluationDRHandler().get_all_annotation_files(['tmp.txt'])

    i = []
    f = []

    for file in annotation_files:
        for name in file['global']:
            item = file['global'][name]
            num_ids = len(item['uniqueIDs'])
            type = item['type']
            if type == 'Identifier':
                i.append(num_ids)
            else:
                f.append(num_ids)

    return {'identifiers': i, 'formulae': f}


def multiple_occurences_total_count(l):
    count = {}
    for num in l:
        if num in count:
            count[num] += 1
        else:
            count[num] = 1

    sorted_list = []
    for k in sorted(count.keys()):
        sorted_list.append([k, count[k]])
    csv_string = list_to_csv(sorted_list)
    total_count = sum([l[0]*l[1] for l in sorted_list])
    return (total_count, csv_string)



test = {'identifiers': [2, 1, 1, 1, 1, 1, 2, 3, 5, 8, 8, 9, 12, 14, 36, 22, 35, 34, 17, 36, 9, 27, 3, 3, 4, 2, 6, 1, 4, 5, 2, 2, 3, 2, 3, 1, 3, 7, 3, 1, 3, 4, 3, 6, 1, 6, 19, 7, 18, 3, 5, 4, 5, 4, 3, 1, 3, 4, 4, 1, 2, 4, 1, 1, 5, 2, 28, 5, 2, 23, 13, 14, 29, 6, 18, 22, 6, 7, 21, 1], 'formulae': [2, 2, 2, 2, 2, 2, 4, 2, 3, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 5, 2, 3, 5, 3, 3, 3, 3, 3, 3]}





if __name__ == '__main__':


    print(multiple_occurences_total_count(test['identifiers']))
    print(multiple_occurences_total_count(test['formulae']))

    """commit_one_eval_file()
    eval_file = get_one_evaluation_file()
    formulae, identifiers = split_formulae_identifiers(eval_file)

    si = selection_rankging_sources_identifiers(identifiers)
    sf = selection_ranking_sources_formulae(formulae)
    print('Selection Ranking: ')
    print('Identifiers: {}'.format(si))
    print('Formulae: {}'.format(sf))
    print()

    lvgi = local_vs_global(identifiers)
    lvgf = local_vs_global(formulae)
    print('Local vs Global: ')
    print('Identifiers: {}'.format(lvgi))
    print('Formulae: {}'.format(lvgf))
    print()

    avg_selection_time_i = average_selection_time(identifiers)
    avg_selection_time_f = average_selection_time(formulae)
    print('Avg selection time: ')
    print('Identifiers: {}'.format(avg_selection_time_i))
    print('Formulae: {}'.format(avg_selection_time_f))
    print()

    avg_manual_selection_time_i = average_manual_time(identifiers)
    avg_manual_selection_time_f = average_manual_time(formulae)
    print('Avg manual seclection time: ')
    print('Identifiers: {}'.format(avg_manual_selection_time_i))
    print('Formulae: {}'.format(avg_manual_selection_time_f))
    print()

    qid_available_i = proportion_qid_available(identifiers)
    qid_available_f = proportion_qid_available(formulae)
    print('QID available: ')
    print('Identifiers: {}'.format(qid_available_i))
    print('Formulae: {}'.format(qid_available_f))
    print()

    multiple_occurrences = time_saved_through_global()
    print('Time saved through global (multiple occurrences): ')
    print(multiple_occurrences)"""



