from django.shortcuts import render
from django.views.generic import View
from ..forms.uploadfileform import UploadFileForm
from ..forms.save_annotation_form import SaveAnnotationForm
from ..latexprocessing.latexprocessor import LaTeXProcessor
from .render_file_view import RenderFileView



class FileUploadView(View):
    form_class = UploadFileForm
    initial = {'key': 'value'}
    template_name = 'file_upload_template.html'
    latexile = None

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #TODO add check to see whether file is .tex
            latexprocessor = LaTeXProcessor(request.FILES['file'])
            self.latexile = latexprocessor.get_latex_file()
            return render(request,
                          'render_file_modal_2.html',
                          {'TexFile': latexprocessor.get_latex_file()})

        return render(request, "file_upload_template.html", self.initial)


    def post(self, request, *args, **kwargs):
        if 'file_submit' in request.POST:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                #TODO add check to see whether file is .tex
                latexprocessor = LaTeXProcessor(request.FILES['file'])
                return render(request,
                              'render_file_modal_2.html',
                              {'TexFile': latexprocessor.get_latex_file()})

            return render(request, "file_upload_template.html", self.initial)

        elif 'data_sub' in request.POST:
            print('in data sub')
            form = SaveAnnotationForm(request.POST)
            if form.is_valid():
                #return render(request, 'render_file_modal_2.html')
                pass

            else:
                print('not valid')
                print(self.latexile)

            return render(request, 'render_file_modal_2.html', {'TexFile': self.latexile})

        return render(request, "file_upload_template.html", self.initial)
