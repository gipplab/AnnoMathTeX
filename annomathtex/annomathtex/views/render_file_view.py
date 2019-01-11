from django.shortcuts import render
from django.views.generic import View
from ..forms.save_annotation_form import SaveAnnotationForm



class RenderFileView(View):

    def __init__(self, request, dict):
        self.request = request
        self.dict = dict
        self.form_class = SaveAnnotationForm
        self.initial = {'key': 'value'}
        self.template_name = 'render_file_modal_2.html'

    def get(self, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(self.request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        pass
