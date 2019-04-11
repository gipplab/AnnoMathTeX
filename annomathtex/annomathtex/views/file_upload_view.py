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
import logging
from ..parsing.txt_parser import TXTParser
from ..parsing.tex_parser import TEXParser
from ..recommendation.arxiv_evaluation_handler import ArXivEvaluationListHandler
from ..recommendation.wikipedia_evaluation_handler import WikipediaEvaluationListHandler
from ..config import recommendations_limit, create_annotation_file_path
from itertools import zip_longest

logging.basicConfig(level=logging.INFO)
__LOGGER__ = logging.getLogger(__name__)

__MARKED__ = {}
__UNMARKED__ = {}
__ANNOTATED__ = {}


class FileUploadView(View):
    """
    This view is where everything going on in the frontend is handled.
    """
    form_class = UploadFileForm
    initial = {'key': 'value'}
    save_annotation_form = {'form': SaveAnnotationForm()}
    template_name = 'file_upload_template.html'

    def get_concatenated_recommendations(self, wikidata_results, arXiv_evaluation_items,
                                         wikipedia_evaluation_items, word_window):
        """
        Concatenate the recommendations from the various sources and show them in the first column.
        #todo: active learner
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
        """
        This method produces the word window for a selected (by the user) formula or identifier. It iteratively takes
        named entities from the lines before and after the selected token(s) to fill the number of named entities as
        specified by the recommendation limit.
        :param unique_id: The unique id if the token (identifier or formula).
        :return: a list of named entities that appear around the selected token.
        """

        word_window = []
        limit = int(recommendations_limit / 2)

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

        return word_window[:recommendations_limit]


    def handle_file_submit(self, request):
        """
        In this method the user selected file is checked for the type of the file (txt, tex, html,...) and the
        appropriate parser for the file type is selected. After the file is processed by the parser it is returned to
        the frontend for rendering.

        The dictionaries __LINE__DICT__ and __IDENTIFIER_LINE_DICT__ are needed for the creation of the word window
        surrounding a token (it is constructed when the user mouse clicks a token (identifier or formula).

        __LINE__DICT__ is a dictionary of line numbers as keys and a list of the named entities that appear on the

        __IDENTIFIER_LINE_DICT__ is a dictionary of the unique ids of identifiers as keys and the line number they
        appear on as values.

        :param request: Request object. Request made by the user through the frontend.
        :return:
        """
        global __LINE__DICT__, __IDENTIFIER_LINE_DICT__
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

            __LINE__DICT__, __IDENTIFIER_LINE_DICT__ = line_dict, identifier_line_dict

            return render(request,
                          'annotation_template.html',
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
        marked = items['marked']
        unmarked = items['unmarked']
        annotated = items['annotated']
        file_name = items['fileName']['f']


        __MARKED__.update(marked)
        __UNMARKED__.update(unmarked)
        __ANNOTATED__.update(annotated)
        __LOGGER__.debug(' ANNOTATED: {}'.format(annotated))


        annotation_file_name = create_annotation_file_path(file_name)
        with open(annotation_file_name, 'w') as f:
            json.dump(__ANNOTATED__, f)

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
            - ArXiv evaluation list is checked for matches
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
        __LOGGER__.debug('in post')
        if 'file_submit' in request.POST:
            return self.handle_file_submit(request)

        elif 'marked' in request.POST:
            return self.handle_marked(request)


        elif 'queryDict' in request.POST:
            return self.handle_query_dict(request)

        return render(request, "file_upload_template.html", self.initial)
