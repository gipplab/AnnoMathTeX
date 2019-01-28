from django.shortcuts import render
from django.views.generic import View
from ..forms.uploadfileform import UploadFileForm
from ..forms.save_annotation_form import SaveAnnotationForm
from ..latexprocessing.process_latex_file import get_processed_file
from django.http import HttpResponse
from ..forms.testform import TestForm
from jquery_unparam import jquery_unparam
import json





__HIGHLIGHT__ = {}
__ANNOTATED__ = {}


class FileUploadView(View):
    form_class = UploadFileForm
    initial = {'key': 'value'}
    save_annotation_form = {'form': SaveAnnotationForm()}
    template_name = 'file_upload_template.html'

    def get(self, request, *args, **kwargs):
        form = TestForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        print('in post')
        for key, value in request.POST.items():
            print('key: ', key)
            print('value: ', jquery_unparam(value))
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

        elif 'highlighted' in request.POST:
            items = request.POST.items()
            print('in data sub')

            return HttpResponse(
                json.dumps({'testkey': 'testvalue'}),
                content_type='application/json'
            )


        return render(request, "file_upload_template.html", self.initial)
