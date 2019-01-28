from django.shortcuts import render
from django.views.generic import View
from ..forms.save_annotation_form import SaveAnnotationForm



class RenderFileView(View):

    form_class = SaveAnnotationForm
    initial = {'key': 'value'}
    template_name = 'render_file_old.html'

    """def __init__(self, latexfile):
        self.latexfile = latexfile
        self.form_class = SaveAnnotationForm
        self.initial = {'key': 'value'}
        self.template_name = 'render_file_old.html'"""

    def get(self, request, *args, **kwargs):
        #form = self.form_class(initial=self.initial)
        form = SaveAnnotationForm()
        latexfile = request.session['latexfile']
        return render(request,
                      self.template_name,
                      {'form': form, 'TexFile': latexfile})

    def post(self, request, *args, **kwargs):
        form = SaveAnnotationForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            return render(request, 'render_file_old.html')

        return render(request, 'render_file_old.html')
