from django.shortcuts import render
from django.views.generic import View
from ..forms.uploadfileform import UploadFileForm
from ..forms.save_annotation_form import SaveAnnotationForm
from ..recommendation.math_sparql import MathSparql
from ..recommendation.ne_sparql import NESparql
from django.http import HttpResponse
from ..forms.testform import TestForm
from jquery_unparam import jquery_unparam
import json
from ..parsing.html_parser import preprocess
import logging
from ..parsing.txt_parser import TXTParser
from ..parsing.tex_parser import TEXParser
from ..recommendation.arxiv_evaluation_handler import ArXivEvaluationListHandler
from ..recommendation.wikipedia_evaluation_handler import WikipediaEvaluationListHandler
from ..config import recommendations_limit
from itertools import zip_longest

logging.basicConfig(level=logging.INFO)
__LOGGER__ = logging.getLogger(__name__)

__MARKED__ = {}
__UNMARKED__ = {}
__ANNOTATED__ = {}


class FileUploadView(View):
    form_class = UploadFileForm
    initial = {'key': 'value'}
    save_annotation_form = {'form': SaveAnnotationForm()}
    template_name = 'file_upload_template.html'
    recommendations_limit = 10

    def decode(self, request_file):
        """
        TeX evaluation_files are in bytes and have to be converted to string in utf-8
        :return: list of lines (string)
        """
        bytes = request_file.read()
        string = bytes.decode('utf-8')
        return string

    def read(self, request_file):
        string = request_file.read()
        return string


    def get_concatenated_recommendations(self, wikidata_results, arXiv_evaluation_items,
                                         wikipedia_evaluation_items, word_window):
        """
        Concatenate the recommendations and show them in the first column
        #todo: active learner
        :param wikidata_results:
        :param arXiv_evaluation_items:
        :param wikipedia_evaluation_items:
        :param word_window:
        :return:
        """

        all_recommendations = zip_longest(
                                              wikidata_results,
                                              arXiv_evaluation_items,
                                              wikipedia_evaluation_items,
                                              word_window,
                                              fillvalue={'name':'__FOO__'}
                                          )
        count = 0
        seen = ['__FOO__']
        concatenated_recommendations = []
        for zip_r in all_recommendations:
            for r in zip_r:
                if count == recommendations_limit: break
                if r['name'] not in seen:
                    concatenated_recommendations.append(r)
                    seen.append(r['name'])
                    count += 1


        return concatenated_recommendations

    def get_word_window(self, unique_id):
        word_window = []
        limit = int(self.recommendations_limit / 2)

        if unique_id in __IDENTIFIER_LINE_DICT__:
            line_num = __IDENTIFIER_LINE_DICT__[unique_id]

        else:
            return []

        i = 0
        #todo: fix
        while i < limit:
            # lines before
            b = line_num - i
            # lines after
            a = line_num + i

            if b in __LINE__DICT__:
                for word in reversed(__LINE__DICT__[b]):
                    # value not yet in word window
                    if not list(filter(lambda d: d['name'] == word.content, word_window)):
                        word_window.append({
                            'name': word.content,
                            #'unique_id': word.unique_id
                        })
                        i += 1
            if a in __LINE__DICT__:
                for word in reversed(__LINE__DICT__[a]):
                    # value not yet in word window
                    if not list(filter(lambda d: d['name'] in word.content, word_window)):
                        word_window.append({
                            'name': word.content,
                            #'unique_id': word.unique_id
                        })
            i += 1

        if not word_window:
            word_window = [{}]

        return word_window[:10]

    def get(self, request, *args, **kwargs):
        form = TestForm()
        return render(request, self.template_name, {'form': form})



    def post(self, request, *args, **kwargs):
        __LOGGER__.debug('in post')
        global __LINE__DICT__, __IDENTIFIER_LINE_DICT__
        if 'file_submit' in request.POST:
            __LOGGER__.debug('file submit')
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                request_file = request.FILES['file']
                file_name = str(request_file)
                if file_name.endswith('.tex'):
                    __LOGGER__.info(' tex file ')
                    line_dict, identifier_line_dict, processed_file = TEXParser(request_file).process()
                    #global __LINE__DICT__, __IDENTIFIER_LINE_DICT__
                    __LINE__DICT__ = line_dict
                    __IDENTIFIER_LINE_DICT__ = identifier_line_dict
                elif file_name.endswith('.html'):
                    decoded_file = self.decode(request_file)
                    preprocessed_file = preprocess(decoded_file)
                    processed_file=None
                elif file_name.endswith('.txt'):
                    __LOGGER__.info(' text file ')
                    line_dict, identifier_line_dict, processed_file = TXTParser(request_file, 'txt').process()
                    #global __LINE__DICT__, __IDENTIFIER_LINE_DICT__
                    __LINE__DICT__ = line_dict
                    __IDENTIFIER_LINE_DICT__ = identifier_line_dict

                #print(processed_file.linked_words)
                #print(processed_file.linked_math_symbols)

                return render(request,
                              'real_time_wikidata_template.html',
                              {'File': processed_file})

            return render(request, "render_file_template.html", self.save_annotation_form)

        elif 'marked' in request.POST:
            items = {k:jquery_unparam(v) for (k,v) in request.POST.items()}
            marked = items['marked']
            unmarked = items['unmarked']
            annotated = items['annotated']

            #todo: write to database
            __MARKED__.update(marked)
            __UNMARKED__.update(unmarked)
            __ANNOTATED__.update(annotated)

            return HttpResponse(
                json.dumps({'testkey': 'testvalue'}),
                content_type='application/json'
            )


        elif 'queryDict' in request.POST:
            __LOGGER__.debug('making wikidata query...')
            items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
            search_string = [k for k in items['queryDict']][0]
            token_type_dict = items['tokenType']
            token_type = [k for k in token_type_dict][0]
            unique_id = [k for k in items['uniqueId']][0]

            concatenated_results, wikidata_results, word_window, \
                arXiv_evaluation_items, wikipedia_evaluation_items = None, None, None, None, None


            if token_type == 'Identifier':
                wikidata_results = MathSparql().identifier_search(search_string)
                arXiv_evaluation_list_handler = ArXivEvaluationListHandler()
                wikipedia_evaluation_list_handler = WikipediaEvaluationListHandler()
                arXiv_evaluation_items = arXiv_evaluation_list_handler.check_identifiers(search_string)
                wikipedia_evaluation_items = wikipedia_evaluation_list_handler.check_identifiers(search_string)
                word_window = self.get_word_window(unique_id)
                concatenated_results = self.get_concatenated_recommendations(
                                                                                wikidata_results,
                                                                                arXiv_evaluation_items,
                                                                                wikipedia_evaluation_items,
                                                                                word_window
                                                                            )
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

                wikidata_results = MathSparql().aliases_search(math_env)

            return HttpResponse(
                json.dumps({'concatenatedResults': concatenated_results,
                            'wikidataResults': wikidata_results,
                            'arXivEvaluationItems': arXiv_evaluation_items,
                            'wikipediaEvaluationItems': wikipedia_evaluation_items,
                            'wordWindow': word_window}),
                content_type='application/json'
            )

        return render(request, "file_upload_template.html", self.initial)
