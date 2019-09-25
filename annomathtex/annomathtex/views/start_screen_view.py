import json
import pickle

from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from ..forms.testform import TestForm
from jquery_unparam import jquery_unparam

from ..forms.uploadfileform import UploadFileForm

from ..parsing.wikipedia_parser import WikipediaParser
from ..views.helper_classes.wikipedia_api_handler import WikipediaAPIHandler
from ..views.helper_classes.data_repo_handler import DataRepoHandler
from ..views.helper_classes.repo_content_handler import RepoContentHandler
from ..views.helper_classes.wikipedia_query_handler import WikipediaQueryHandler
from ..views.helper_classes.wikipedia_article_handler import WikipediaArticleHandler

from ..config import *


class StartScreenView(View):

    form_class = UploadFileForm
    initial = {'key': 'value'}
    template_name = 'file_upload_wiki_suggestions_2.html'

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
        if 'wikipediaArticleName' in request.POST:
            print('wikipediaArticleName')
            return WikipediaArticleHandler(request).get_rendered_wikipedia_article()

        elif 'getRepoContent' in request.POST:
            print('getRepoContent')
            return RepoContentHandler().get_repo_content()

        elif 'wikipediaSubmit' in request.POST:
            print("WIKIPEDIA SUBMIT")
            return WikipediaQueryHandler(request).get_suggestions()

        elif 'addArticleToRepo' in request.POST:
            print('addArticleToRepo')
            return WikipediaArticleHandler(request).add_wikipedia_article(self.template_name, TestForm())

        return render(request, "file_upload_wiki_suggestions_2.html", self.initial)

