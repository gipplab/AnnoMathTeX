from django.shortcuts import render
from django.views.generic import View



class FileUploadView(View):
    initial = {'key': 'value'}
    template_name = 'render_file_modal.html'

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
