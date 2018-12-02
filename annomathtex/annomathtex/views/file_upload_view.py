from django.shortcuts import render
from django.views.generic import View
from ..latexprocessing.latexfile import LaTexFile
from ..forms.uploadfileform import UploadFileForm



class FileUploadView(View):
    form_class = UploadFileForm
    initial = {'key': 'value'}
    template_name = 'file_upload_template.html'


    """def get(self, request, *args, **kwargs):
        #context = {'TexFile': TexFile()}
        lines_string = ""
        if 'myfile' in request.GET:
            with open(request.GET['myfile']) as file:
                lines_string = file.read()

        context = {'TexFile': lines_string}
        return render(request, "file_upload_template.html", context)"""

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES['file'])
            uploaded_file = request.FILES['file']
            print(uploaded_file.read())

        # for word in TexFile().body:
        #    print(word.content)
        # print(TexFile().body)
        return render(request, "file_upload_template.html", self.initial)
