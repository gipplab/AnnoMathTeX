from django.shortcuts import render
from django.http import HttpResponse
from jquery_unparam import jquery_unparam
from ..forms.uploadfileform import UploadFileForm
from ..forms.save_annotation_form import SaveAnnotationForm
from ..parsing.txt_parser import TXTParser
from ..parsing.tex_parser import TEXParser
from ..recommendation.math_sparql import MathSparql
from ..recommendation.ne_sparql import NESparql
import logging
import json

#todo: implement
class PostHelper:

    def __init__(self, request):
        self.request = request
        logging.basicConfig(level=logging.INFO)
        # dictConfig(logging_config_path)
        self.__LOGGER__ = logging.getLogger(__name__)


    def handle_file_submit(self):
        form = UploadFileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            request_file = self.request.FILES['file']
            file_name = str(request_file)
            if file_name.endswith('.tex'):
                self.__LOGGER__.info(' tex file ')
                processed_file = TEXParser(request_file).process()
            elif file_name.endswith('.html'):
                #not supported atm
                pass
            elif file_name.endswith('.txt'):
                # assuming it's a txt file
                self.__LOGGER__.info(' text file ')
                processed_file = TXTParser(request_file).process()

            return render(self.request,
                          'real_time_wikidata_template.html',
                          {'File': processed_file})
        save_annotation_form = {'form': SaveAnnotationForm()}
        return render(self.request, "render_file_template.html", save_annotation_form)

    def handle_marked(self):
        items = {k: jquery_unparam(v) for (k, v) in self.request.POST.items()}
        marked = items['marked']
        annotatedQID = items['annotatedQID']
        annotatedWW = items['annotatedWW']
        unmarked = items['unmarked']

        self.__LOGGER__.debug('marked {}'.format(marked))
        self.__LOGGER__.debug('marked {}'.format(annotatedQID))
        self.__LOGGER__.debug('marked {}'.format(annotatedWW))
        self.__LOGGER__.debug('marked {}'.format(unmarked))

        # todo: write to database
        #__MARKED__.update(marked)
        #__ANNOTATED_QID__.update(annotatedQID)
        #__ANNOTATED_WW__.update(annotatedWW)
        #__UNMARKED__.update(unmarked)

        return HttpResponse(
            json.dumps({'testkey': 'testvalue'}),
            content_type='application/json'
        )

    def handle_query_dict(self):
        self.__LOGGER__.info('making wikidata query...')
        items = {k: jquery_unparam(v) for (k, v) in self.request.POST.items()}
        search_string = [k for k in items['queryDict']][0]
        token_type_dict = items['tokenType']
        token_type = [k for k in token_type_dict][0]

        if token_type == 'Identifier':
            wikidata_results = MathSparql().identifier_search(search_string)
        elif token_type == 'Word':
            wikidata_results = NESparql().named_entity_search(search_string)
        elif token_type == 'Formula':
            m = items['mathEnv']
            k = list(m.keys())[0]
            if m[k]:
                math_env = k + '=' + m[k]
            else:
                math_env = k

            self.__LOGGER__.debug('math_env: {}'.format(math_env))

            wikidata_results = MathSparql().aliases_search(math_env)
        else:
            wikidata_results = None

        return HttpResponse(
            json.dumps({'wikidataResults': wikidata_results}),
            content_type='application/json'
        )


    def process_request(self):

        if 'file_submit' in self.request.POST:
            self.__LOGGER__.info(' file submit ')
            response = self.handle_file_submit()

        elif 'marked' in self.request.POST:
            self.__LOGGER__.info(' marked ')
            response = self.handle_marked()

        elif 'queryDict' in self.request.POST:
            self.__LOGGER__.info(' query dict ')
            response = self.handle_query_dict()

        return response
