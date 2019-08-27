import json
import pickle

from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from ..forms.testform import TestForm
from jquery_unparam import jquery_unparam

from ..forms.uploadfileform import UploadFileForm


from ..config import *


class TestView(View):

    form_class = UploadFileForm
    initial = {'key': 'value'}
    template_name = 'test_template.html'


    def get(self, request, *args, **kwargs):
        """
        This method handles get request from the frontend.
        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name and the necessary form.
        """
        form = TestForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        """
        This method handles post request from the frontend. Any data being passed to the backend will be passed through
        a post request, meaning that this method will be called for all tasks that require the frontend in any way to
        access the backend.
        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name, the necessary form and the response data (if
                 applicable).
        """
        return render(request, "test_template.html", self.initial)

