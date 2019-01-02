from django.shortcuts import render
from django.views.generic import View
from ..forms.uploadfileform import UploadFileForm
from ..latexprocessing.latexprocessor import LaTeXProcessor



class FileUploadView(View):
    form_class = UploadFileForm
    initial = {'key': 'value'}
    template_name = 'file_upload_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #TODO add check to see whether file is .tex
            latexprocessor = LaTeXProcessor(request.FILES['file'])
            return render(request,
                          #'render_file_template.html',
                          'render_file_template_2.html',
                          {'TexFile': latexprocessor.get_latex_file()})

        return render(request, "file_upload_template.html", self.initial)
