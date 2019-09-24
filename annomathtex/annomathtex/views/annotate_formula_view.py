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
from ..parsing.wikipedia_parser import WikipediaParser
from ..recommendation.arxiv_evaluation_handler import ArXivEvaluationListHandler
from ..recommendation.wikipedia_evaluation_handler import WikipediaEvaluationListHandler
from ..recommendation.static_wikidata_handler import StaticWikidataHandler
from ..recommendation.manual_recommendations_handler import ManualRecommendationsHandler
from ..recommendation.formula_concept_db_handler import FormulaConceptDBHandler
from ..forms.uploadfileform import UploadFileForm
from ..forms.save_annotation_form import SaveAnnotationForm
from ..recommendation.math_sparql import MathSparql
from ..recommendation.ne_sparql import NESparql

from ..views.eval_file_writer import EvalFileWriter
from ..views.data_repo_handler import DataRepoHandler, FormulaConceptHandler, ManualRecommendationsCleaner
from ..views.wikipedia_api_handler import WikipediaAPIHandler
from .helper_functions import handle_annotations
from ..config import *

from .helper_classes.token_clicked_handler import TokenClickedHandler
from .helper_classes.file_handler import FileHandler
from .helper_classes.cache_handler import CacheHandler
from .helper_classes.wikipedia_query_handler import WikipediaQueryHandler


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
    #template_name = 'file_upload_wiki_suggestions_2.html'
    template_name = 'annotation_template_tmp.html'

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

    def read_file_name_cache(self):
        if os.path.isfile(file_name_cache_path):
            with open(file_name_cache_path, 'r') as infile:
                file_name = infile.read()
        else:
            with open(file_name_cache_path_deployed_sys, 'r') as infile:
                file_name = infile.read()
        return file_name


    def write_file_name_cache(self, file_name):
        if os.path.isfile(file_name_cache_path):
            with open(file_name_cache_path, 'w') as outfile:
                outfile.truncate(0)
                outfile.write(file_name)
        else:
            with open(file_name_cache_path_deployed_sys, 'w') as outfile:
                outfile.truncate(0)
                outfile.write(file_name)
        return


    def handle_marked(self, request):
        """
        This method receives data from the frontend, when the user mouse clicks the "save" button.

        Annotated items: e.g. the user annotated the identifier "E" with the wikidata item "energy (Q11379)".
        Marked items: A word that wasn't found by the named entity tagger, but the user decided it should have been.
        Unmarked items: A Word that was found by the named entity tagger, but the user decided it shouldn't have been.

        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name and the necessary form.
        """
        print('IN HANDLE MARKED')
        items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
        annotations = items['annotations']
        file_name = items['fileName']['f']
        manual_recommendations = items['manualRecommendations']

        #print(annotations)


        m = ManualRecommendationsCleaner(manual_recommendations)
        cleaned_manual_recommendations = m.get_recommendations()


        new_annotations = handle_annotations(annotations)

        annotation_file_path = create_annotation_file_path(file_name)
        with open(annotation_file_path, 'w') as f:
            __LOGGER__.debug(' WRITING TO FILE {}'.format(annotation_file_path))
            json.dump(new_annotations, f)


        eval_file_writer = EvalFileWriter(new_annotations, file_name)
        #eval_file_writer.write()
        evaluation_csv_string = eval_file_writer.get_csv_for_repo()
        data_repo_handler = DataRepoHandler()
        #file_name = re.sub(r'\..*', '.csv', file_name)

        annotation_file_name = create_annotation_file_name(file_name)
        evaluation_file_name = create_evaluation_file_name(file_name)
        data_repo_handler.commit_manual_recommendations(cleaned_manual_recommendations)
        data_repo_handler.commit_formula_concepts(annotations)
        data_repo_handler.commit_annotations(annotation_file_name, json.dumps(annotations))
        data_repo_handler.commit_evaluation(evaluation_file_name, evaluation_csv_string)

        return HttpResponse(
            json.dumps({'testkey': 'testvalue'}),
            content_type='application/json'
        )


    def handle_wikipedia_query(self, request):
        items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
        search_string = list(items['wikipediaSubmit'].keys())[0]
        w = WikipediaAPIHandler()
        r = w.get_suggestions(search_string)
        return HttpResponse(
                            json.dumps({'wikipediaResults': r}),
                            content_type='application/json')


    def get_repo_content(self):
        """
        Get the repo content for the datarepo/annotation folder, i.e. all files that have been annotated in the past.
        :return:
        """
        file_names = DataRepoHandler().list_directory()
        return HttpResponse(
                            json.dumps({'fileNames': file_names}),
                            content_type='application/json'
        )


    def get(self, request, *args, **kwargs):
        """
        This method handles get request from the frontend.
        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name and the necessary form.
        """
        article_name = CacheHandler().read_file_name_cache()
        processed_file = FileHandler(request).get_processed_wikipedia_article(article_name)
        return render(request, self.template_name, {'File': processed_file, 'test': 3})



    def post(self, request, *args, **kwargs):
        """
        This method handles post request from the frontend. Any data being passed to the backend will be passed through
        a post request, meaning that this method will be called for all tasks that require the frontend in any way to
        access the backend.
        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name, the necessary form and the response data (if
                 applicable).
        """
        #items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
        #print(items)

        if 'file_submit' in request.POST:
            return FileHandler(request).process_local_file()

        elif 'queryDict' in request.POST:
            print('queryDict')
            return TokenClickedHandler(request).get_recommendations()

        elif 'annotations' in request.POST:
            print('annotations')
            return self.handle_marked(request)

        #todo: remove this method from this view (and others that aren't used)
        #todo: check if not used
        elif 'wikipediaSubmit' in request.POST:
            print("WIKIPEDIA SUBMIT")
            #return self.handle_wikipedia_query(request)
            return WikipediaQueryHandler(request).get_suggestions()

        elif 'wikipediaArticleName' in request.POST:
            #todo: put in separate method (consistency)
            items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
            article_name = list(items['wikipediaArticleName'].keys())[0]
            self.write_file_name_cache(article_name)
            return render(request, "annotation_template_tmp.html", self.initial)



        elif 'getRepoContent' in request.POST:
            print('getRepoContent')
            return self.get_repo_content()



        return render(request, "file_upload_wiki_suggestions_2.html", self.initial)
