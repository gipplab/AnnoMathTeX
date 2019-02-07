from django.shortcuts import render
from django.views.generic import View
from ..forms.uploadfileform import UploadFileForm
from ..forms.save_annotation_form import SaveAnnotationForm
#from ..latexprocessing.process_latex_file import get_processed_file
from ..latexprocessing.process_latex_file_new import get_processed_file
from ..latexprocessing.math_environment_handling import MathSparql
from ..latexprocessing.named_entity_handling import NESparql
from django.http import HttpResponse
from ..forms.testform import TestForm
from jquery_unparam import jquery_unparam
import json
from django.views.decorators.csrf import csrf_protect




__HIGHLIGHTED__ = {}
__ANNOTATED_QID__ = {}
__ANNOTATED_NE__ = {}


class FileUploadView(View):
    form_class = UploadFileForm
    initial = {'key': 'value'}
    save_annotation_form = {'form': SaveAnnotationForm()}
    template_name = 'file_upload_template.html'

    def get(self, request, *args, **kwargs):
        form = TestForm()
        return render(request, self.template_name, {'form': form})

    #@csrf_protect
    def post(self, request, *args, **kwargs):

        print('IN POST')

        #for k, v in request.POST.items():
        #    print(k, v)

        if 'file_submit' in request.POST:
            print('in file submit')
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                #TODO add check to see whether file is .tex
                #latex_file = get_processed_file(request.FILES['file'])
                latex_file = get_processed_file(request.FILES['file'])
                return render(request,
                              #'render_file_old.html',
                              #'render_file_template.html',
                              #'test_template_d3.html',
                              'real_time_wikidata_template.html',
                              {'TexFile': latex_file})

            return render(request, "render_file_template.html", self.save_annotation_form)

        elif 'highlighted' in request.POST:
            print('in highlighted')
            items = {k:jquery_unparam(v) for (k,v) in request.POST.items()}
            highlighted = items['highlighted']
            annotatedQID = items['annotatedQID']
            annotatedNE = items['annotatedNE']

            print(highlighted)
            print(annotatedQID)
            print(annotatedNE)


            #todo: write to database
            __HIGHLIGHTED__.update(highlighted)
            __ANNOTATED_QID__.update(annotatedQID)
            __ANNOTATED_NE__.update(annotatedNE)

            #print('__HIGHLIGHTED__: ', __HIGHLIGHTED__)
            #print('__ANNOTATED__: ', __ANNOTATED__)




            return HttpResponse(
                json.dumps({'testkey': 'testvalue'}),
                content_type='application/json'
            )


        #make wikidata queries in real time
        elif 'queryDict' in request.POST:
            print('Wikidata Query made')
            items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
            #for k in items:
            #    print(k, items[k])
            query_dict = items['queryDict']
            search_string = [k for k in query_dict][0]
            token_type_dict = items['tokenType']
            token_type = [k for k in token_type_dict][0]
            #print('SEARCH STRING: ', search_string)

            if token_type == 'Identifier':
                wikidata_results = MathSparql().broad_search(search_string)
            #could change this to only allow named entitiy searches
            elif token_type == 'Word':
                wikidata_results = NESparql().named_entity_search(search_string)
                #print(wikidata_results)
            else:
                wikidata_results = None

            return HttpResponse(
                json.dumps({'wikidataResults': wikidata_results}),
                content_type='application/json'
            )



        return render(request, "file_upload_template.html", self.initial)
