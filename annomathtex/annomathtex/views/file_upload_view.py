from django.shortcuts import render
from django.views.generic import View
from ..latexprocessing.latexfile import LaTexFile
from ..forms.filepathform import FilePathForm



class FileUploadView(View):

    def get(self, request, *args, **kwargs):
        #context = {'TexFile': TexFile()}
        lines_string = ""
        if 'myfile' in request.GET:
            with open(request.GET['myfile']) as file:
                lines_string = file.read()

        context = {'TexFile': lines_string}
        return render(request, "file_upload_template.html", context)

    def post(self, request, *args, **kwargs):
        print('FRONTRENDER POST1')
        context = {'TexFile': LaTexFile()}
        if request.method == 'POST':
            print('POST2')
            request.POST.get('path')
            form = FilePathForm(request.POST)
            if form.is_valid():
                print(form)
            # return render(request, "front-end-render.html", context)

        # for word in TexFile().body:
        #    print(word.content)
        # print(TexFile().body)
        return render(request, "file_upload_template.html", context)
