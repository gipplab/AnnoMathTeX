import json
import logging
import pickle
import re

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from ..forms.testform import TestForm
from jquery_unparam import jquery_unparam
from itertools import zip_longest
from time import time

from ..parsing.txt_parser import TXTParser
from ..parsing.tex_parser import TEXParser
from ..recommendation.arxiv_evaluation_handler import ArXivEvaluationListHandler
from ..recommendation.wikipedia_evaluation_handler import WikipediaEvaluationListHandler
from ..recommendation.static_wikidata_handler import StaticWikidataHandler
from ..recommendation.manual_recommendations_handler import ManualRecommendationsHandler
from ..forms.uploadfileform import UploadFileForm
from ..forms.save_annotation_form import SaveAnnotationForm
from ..recommendation.math_sparql import MathSparql
from ..recommendation.ne_sparql import NESparql

from ..views.eval_file_writer import EvalFileWriter
from ..views.data_repo_handler import DataRepoHandler, FormulaConceptHandler, ManualRecommendationsCleaner
from .helper_functions import handle_annotations
from ..config import *


logging.basicConfig(level=logging.INFO)
__LOGGER__ = logging.getLogger(__name__)

__MARKED__ = {}
__UNMARKED__ = {}
__ANNOTATED__ = {}
__LINE_DICTS__ = {}


class FileUploadView(View):
    """
    This view is where everything going on in the frontend is handled.
    """
    form_class = UploadFileForm
    initial = {'key': 'value'}
    save_annotation_form = {'form': SaveAnnotationForm()}
    template_name = 'file_upload_template.html'

    def get_concatenated_recommendations(self, type, wikidata_results, arXiv_evaluation_items,
                                         wikipedia_evaluation_items, word_window):
        """
        Concatenate the recommendations from the various sources and show them in the first column.
        :param wikidata_results: The results that were obtained from querying the wikidata query service API.
        :param arXiv_evaluation_items: The results that were obtained from checking string matches of the character
                                       in the evaluation list from ArXiv. Only for identifiers.
        :param wikipedia_evaluation_items: The results that were obtained from checking string matches of the character
                                           in the evaluation list from Wikipedia. Only for identifiers.
        :param word_window: The named entities (as found by the tagger) that surround the identifier/formula within
                            the text.
        :return: A list of unique results where as long as the source contains more results the order goes Wikidata,
                 ArXiv, Wikipedia, Word Window.
        """


        all_recommendations = zip_longest(
                                              wikidata_results,
                                              arXiv_evaluation_items,
                                              wikipedia_evaluation_items,
                                              word_window,
                                              fillvalue={'name':'__FILLVALUE__'}
                                          )
        count = 0
        seen = ['__FILLVALUE__']
        concatenated_recommendations = []
        for zip_r in all_recommendations:
            #print(zip_r)
            for r in zip_r:
                if count == recommendations_limit: break
                if r['name'] not in seen:
                    if 'qid' not in r:
                        results = NESparql().concatenated_column_search(r['name'])
                        r = results[0] if results else r
                    concatenated_recommendations.append(r)
                    seen.append(r['name'])
                    count += 1


        return concatenated_recommendations

    def get_word_window(self, unique_id):
        """
        This method produces the word window for a selected (by the user) formula or identifier. It iteratively takes
        named entities from the lines before and after the selected token(s) to fill the number of named entities as
        specified by the recommendation limit.
        :param unique_id: The unique id if the token (identifier or formula).
        :return: a list of named entities that appear around the selected token.
        """

        word_window = []
        limit = int(recommendations_limit / 2)
        dicts = self.cache_to_dicts()
        identifier_line_dict = dicts['identifiers']
        line_dict = dicts['lines']
        if unique_id in identifier_line_dict:
            line_num = identifier_line_dict[unique_id]
        else:
            return []

        i = 0
        while i < limit:
            # lines before
            b = line_num - i
            # lines after
            a = line_num + i

            if b in line_dict:
                for word in reversed(line_dict[b]):
                    # value not yet in word window
                    if not list(filter(lambda d: d['name'] == word.content.lower(), word_window)):
                        word_window.append({
                            'name': word.content.lower(),
                            #'unique_id': word.unique_id
                        })
                        i += 1
            if a in line_dict:
                for word in reversed(line_dict[a]):
                    # value not yet in word window
                    if not list(filter(lambda d: d['name'] in word.content.lower(), word_window)):
                        word_window.append({
                            'name': word.content.lower(),
                            #'unique_id': word.unique_id
                        })
            i += 1
        if not word_window:
            word_window = [{}]
        return word_window[:recommendations_limit]

    def dicts_to_cache(self, dicts):
        """
        Write the dictionary, that is used to form the word window when the user clicks a token, to the cache.
        :param dicts: Line dictionary and identifier line dictionary.
        :return: None; files are pickled and stored in cache.
        """
        path = view_cache_path + 'dicts'
        with open(path, 'wb') as outfile:
            pickle.dump(dicts, outfile)
        __LOGGER__.debug(' Wrote file to {}'.format(path))


    def cache_to_dicts(self):
        """
        Read the dictionary, that is used to form the word window when the user clicks a token, from the cache.
        :return: Line dictionary and identifier line dictionary.
        """
        path = view_cache_path + 'dicts'
        with open(path, 'rb') as infile:
            dicts = pickle.load(infile)
        return dicts


    def handle_file_submit(self, request):
        """
        In this method the user selected file is checked for the type of the file (txt, tex, html,...) and the
        appropriate parser for the file type is selected. After the file is processed by the parser it is returned to
        the frontend for rendering.

        The dictionaries line_dict and identifier_line_dict are needed for the creation of the word window
        surrounding a token (it is constructed when the user mouse clicks a token (identifier or formula).

        line_dict is a dictionary of line numbers as keys and a list of the named entities that appear on the

        identifier_line_dict is a dictionary of the unique ids of identifiers as keys and the line number they
        appear on as values.

        :param request: Request object; request made by the user through the frontend.
        :return: The rendered response to the frontend.
        """
        __LOGGER__.debug('file submit')
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            request_file = request.FILES['file']
            file_name = str(request_file)
            if file_name.endswith('.tex'):
                __LOGGER__.info(' tex file ')
                line_dict, identifier_line_dict, processed_file = TEXParser(request_file, file_name).process()
            elif file_name.endswith('.txt'):
                __LOGGER__.info(' text file ')
                line_dict, identifier_line_dict, processed_file = TXTParser(request_file, file_name).process()
            else:
                line_dict, identifier_line_dict, processed_file = None, None, None


            dicts = {'identifiers': identifier_line_dict, 'lines': line_dict}

            self.dicts_to_cache(dicts)



            return render(request,
                          #'annotation_template.html',
                          'annotation_template_tmp.html',
                          {'File': processed_file})


        return render(request, "render_file_template.html", self.save_annotation_form)

    def handle_marked(self, request):
        """
        This method receives data from the frontend, when the user mouse clicks the "save" button.

        Annotated items: e.g. the user annotated the identifier "E" with the wikidata item "energy (Q11379)".
        Marked items: A word that wasn't found by the named entity tagger, but the user decided it should have been.
        Unmarked items: A Word that was found by the named entity tagger, but the user decided it shouldn't have been.

        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name and the necessary form.
        """
        items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
        #marked = items['marked']
        #unmarked = items['unmarked']
        annotations = items['annotations']
        file_name = items['fileName']['f']
        manual_recommendations = items['manualRecommendations']


        m = ManualRecommendationsCleaner(manual_recommendations)
        cleaned_manual_recommendations = m.get_recommendations()


        __LOGGER__.debug(' ITEMS : {}'.format(items))


        new_annotations = handle_annotations(annotations)

        annotation_file_path = create_annotation_file_path(file_name)
        with open(annotation_file_path, 'w') as f:
            __LOGGER__.debug(' WRITING TO FILE {}'.format(annotation_file_path))
            json.dump(new_annotations, f)

        #eval_file_writer = EvalFileWriter(annotations, file_name)
        #eval_file_writer.write()

        #f = FormulaConceptHandler(new_annotations)#.get_formulae()
        #f.handle()

        eval_file_writer = EvalFileWriter(new_annotations, file_name)
        eval_file_writer.write()
        csv_string = eval_file_writer.get_csv_for_repo()
        data_repo_handler = DataRepoHandler()
        file_name = re.sub(r'\..*', '.csv', file_name)
        data_repo_handler.commit_manual_recommendations(cleaned_manual_recommendations)
        data_repo_handler.commit_to_repo(file_name, csv_string, new_annotations)
        data_repo_handler.commit_file(create_annotation_file_name(file_name), json.dumps(annotations))


        return HttpResponse(
            json.dumps({'testkey': 'testvalue'}),
            content_type='application/json'
        )

    def handle_query_dict(self, request):
        """
        This method handles the use case, when the user selects a token (word, identifier or formula) to annotate.
        Depending on the type of the token, different types of data are sent back to the frontend.

        Identifier:
            - Wikidata query is made
            - ArXiv evaluation list is checked for matches8
            - Wikipedia evaluation list is checked for matches
            - Word window is computed

        Formula:
            - Wikidata query is made
            - Word window is computed

        Word (must not necessarily be named entity, as found by tagger):
            - Wikidata query is made


        For identifier and formulae, additionaly the concatenated results are computed, taking results from each of the
        sources and combining them in one column.

        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name, the necessary form and the response data.
        """
        start = time()
        items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
        search_string = [k for k in items['queryDict']][0]
        token_type_dict = items['tokenType']
        token_type = [k for k in token_type_dict][0]
        unique_id = [k for k in items['uniqueId']][0]

        __LOGGER__.debug('making wikidata query for search string: {}'.format(search_string))

        concatenated_results, wikidata_results, word_window, \
        arXiv_evaluation_items, wikipedia_evaluation_items, manual_recommendations = [], [], [], [], [], []#None, None, None, None, None

        if token_type == 'Identifier':
            wikidata_results = StaticWikidataHandler().check_identifiers(search_string)
            arXiv_evaluation_items = ArXivEvaluationListHandler().check_identifiers(search_string)
            wikipedia_evaluation_items = WikipediaEvaluationListHandler().check_identifiers(search_string)
            word_window = self.get_word_window(unique_id)
            manual_recommendations = ManualRecommendationsHandler().check_identifier_or_formula(search_string)
        elif token_type == 'Word':
            wikidata_results = NESparql().named_entity_search(search_string)
        elif token_type == 'Formula':
            m = items['mathEnv']
            k = list(m.keys())[0]
            if m[k]:
                math_env = k + '=' + m[k]
            else:
                math_env = k
            __LOGGER__.debug('math_env: {}'.format(math_env))
            #not static atm
            #could also add .tex_string_search()
            wikidata_results = MathSparql().aliases_search(math_env)
            word_window = self.get_word_window(unique_id)
            manual_recommendations = DataRepoHandler().get_manual_recommendations()
            manual_recommendations = ManualRecommendationsHandler(manual_recommendations).check_identifier_or_formula(search_string)



        __LOGGER__.debug(' wikidata query made in {}'.format(time()-start))

        __LOGGER__.debug(' word window: {}'.format(word_window))
        __LOGGER__.debug(' wikipedia: {}'.format(wikipedia_evaluation_items))
        __LOGGER__.debug(' arxiv: {}'.format(arXiv_evaluation_items))
        __LOGGER__.debug(' wikidata: {}'.format(wikidata_results))

        def fill_to_limit(dict_list):
            dict_list += [{'name': ''} for _ in range(recommendations_limit-len(dict_list))]
            return dict_list


        return HttpResponse(
            json.dumps({'wikidataResults': fill_to_limit(wikidata_results),
                        'arXivEvaluationItems': fill_to_limit(arXiv_evaluation_items),
                        'wikipediaEvaluationItems': fill_to_limit(wikipedia_evaluation_items),
                        'wordWindow': fill_to_limit(word_window),
                        'manual': fill_to_limit(manual_recommendations)}),
            content_type='application/json'
        )

    def get(self, request, *args, **kwargs):
        """
        This method handles get request from the frontend.
        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name and the necessary form.
        """
        form = TestForm()
        return render(request, self.template_name, {'form': form})



    def post(self, request, *args, **kwargs):
        """
        This method handles post request from the frontend. Any data being passed to the backend will be passed through
        a post request, meaning that this method will be called for all tasks that require the frontend in any way to
        access the backend.
        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name, the necessary form and the response data (if
                 applicable).
        """
        __LOGGER__.debug('in post {}'.format(os.getcwd()))
        if 'file_submit' in request.POST:
            return self.handle_file_submit(request)

        elif 'annotations' in request.POST:
            return self.handle_marked(request)


        elif 'queryDict' in request.POST:
            return self.handle_query_dict(request)

        return render(request, "file_upload_template.html", self.initial)
