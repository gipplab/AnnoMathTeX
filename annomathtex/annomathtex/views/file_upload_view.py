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
from .posthelper import PostHelper

logging.basicConfig(level=logging.INFO)
#dictConfig(logging_config_path)
__LOGGER__ = logging.getLogger(__name__)




__MARKED__ = {}
__ANNOTATED_QID__ = {}
__ANNOTATED_WW__ = {}
__UNMARKED__ = {}


class FileUploadView(View):
    form_class = UploadFileForm
    initial = {'key': 'value'}
    save_annotation_form = {'form': SaveAnnotationForm()}
    template_name = 'file_upload_template.html'

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

    def get(self, request, *args, **kwargs):
        form = TestForm()
        return render(request, self.template_name, {'form': form})



    def post(self, request, *args, **kwargs):
        __LOGGER__.debug('in post')
        if 'file_submit' in request.POST:
            __LOGGER__.debug('file submit')
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                request_file = request.FILES['file']
                file_name = str(request_file)
                if file_name.endswith('.tex'):
                    __LOGGER__.info(' tex file ')
                    processed_file = TEXParser(request_file).process()
                elif file_name.endswith('.html'):
                    decoded_file = self.decode(request_file)
                    preprocessed_file = preprocess(decoded_file)
                    processed_file=None
                elif file_name.endswith('.txt'):
                    __LOGGER__.info(' text file ')
                    processed_file = TXTParser(request_file, 'txt').process()

                return render(request,
                              'real_time_wikidata_template.html',
                              {'File': processed_file})

            return render(request, "render_file_template.html", self.save_annotation_form)

        elif 'marked' in request.POST:
            items = {k:jquery_unparam(v) for (k,v) in request.POST.items()}
            marked = items['marked']
            annotatedQID = items['annotatedQID']
            annotatedWW = items['annotatedWW']
            unmarked = items['unmarked']

            __LOGGER__.debug('marked {}'.format(marked))
            __LOGGER__.debug('marked {}'.format(annotatedQID))
            __LOGGER__.debug('marked {}'.format(annotatedWW))
            __LOGGER__.debug('marked {}'.format(unmarked))

            #todo: write to database
            __MARKED__.update(marked)
            __ANNOTATED_QID__.update(annotatedQID)
            __ANNOTATED_WW__.update(annotatedWW)
            __UNMARKED__.update(unmarked)


            return HttpResponse(
                json.dumps({'testkey': 'testvalue'}),
                content_type='application/json'
            )


        #make wikidata queries in real time
        elif 'queryDict' in request.POST:
            __LOGGER__.debug('making wikidata query...')
            items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
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

                __LOGGER__.debug('math_env: {}'.format(math_env))

                wikidata_results = MathSparql().aliases_search(math_env)
            else:
                wikidata_results = None

            return HttpResponse(
                json.dumps({'wikidataResults': wikidata_results}),
                content_type='application/json'
            )

        return render(request, "file_upload_template.html", self.initial)
