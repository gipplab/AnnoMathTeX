from django.shortcuts import render
from django.views.generic import View
from ..forms.uploadfileform import UploadFileForm
from ..forms.save_annotation_form import SaveAnnotationForm
from ..latexprocessing.latexprocessor import LaTeXProcessor
from ..latexprocessing.process_latex_file import get_processed_file
from .render_file_view import RenderFileView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from ..views.render_file_view import RenderFileView
from django.core import serializers
from ..forms.testform import TestForm
import json


#TODO clean up this file
class FileUploadView(View):
    form_class = UploadFileForm
    initial = {'key': 'value'}
    save_annotation_form = {'form': SaveAnnotationForm()}
    template_name = 'file_upload_template.html'

    def get(self, request, *args, **kwargs):
        #form = self.form_class(initial=self.initial)
        #form = self.save_annotation_form
        form = TestForm()
        return render(request, self.template_name, {'form': form})

    """def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #TODO add check to see whether file is .tex
            latexprocessor = LaTeXProcessor(request.FILES['file'])
            self.latexile = latexprocessor.get_latex_file()
            return render(request,
                          'render_file_modal_2.html',
                          {'TexFile': latexprocessor.get_latex_file()})

        return render(request, "file_upload_template.html", self.initial)"""

    """def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            # TODO add check to see whether file is .tex
            #latexprocessor = LaTeXProcessor(request.FILES['file'])
            #latexfile = latexprocessor.get_latex_file()
            #latexfile = serializers.serialize('json', [latexfile, ])
            request.session['latexfile'] = 'test'#latexfile
            return redirect('/render_file/')

        return render(request, "file_upload_template.html", self.initial)"""

    #@csrf_protect
    def post(self, request, *args, **kwargs):
        print('in post')
        for key, value in request.POST.items():
            print('key: ', key)
            print('value: ', value)
            print()
        if 'file_submit' in request.POST:
            print('in file submit')
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                #TODO add check to see whether file is .tex
                #latexprocessor = LaTeXProcessor(request.FILES['file'])
                #latex_file = latexprocessor.get_latex_file()
                latex_file = get_processed_file(request.FILES['file'])
                return render(request,
                              'render_file_modal_2.html',
                              {'TexFile': latex_file})

            return render(request, "file_upload_template.html", self.save_annotation_form)

        elif 'valuepass' in request.POST:
            print('in data sub')
            """form = SaveAnnotationForm(request.POST)
            if form.is_valid():
                print(request.POST.get('hidden_input', None))
                #return render(request, 'render_file_modal_2.html')
                return HttpResponseRedirect('/')

            else:
                print('not valid')
                #print(self.latexile)"""


            #return render(request, 'render_file_modal_2.html', {'TexFile': self.latexile})
            return HttpResponse(
                json.dumps({'testkey': 'testvalue'}),
                content_type='application/json'
            )


        return render(request, "file_upload_template.html", self.initial)
