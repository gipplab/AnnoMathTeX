import json
import pickle

from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from ..forms.testform import TestForm
from jquery_unparam import jquery_unparam

from ..forms.uploadfileform import UploadFileForm

from ..parsing.wikipedia_parser import WikipediaParser
from ..views.wikipedia_api_handler import WikipediaAPIHandler
from ..views.data_repo_handler import DataRepoHandler

from ..config import *


class StartScreenView(View):

    form_class = UploadFileForm
    initial = {'key': 'value'}
    template_name = 'file_upload_wiki_suggestions_2.html'



    def dicts_to_cache(self, dicts):
        """
        Write the dictionary, that is used to form the word window when the user clicks a token, to the cache.
        :param dicts: Line dictionary and identifier line dictionary.
        :return: None; files are pickled and stored in cache.
        """
        path = view_cache_path + 'dicts'
        with open(path, 'wb') as outfile:
            pickle.dump(dicts, outfile)
        #__LOGGER__.debug(' Wrote file to {}'.format(path))


    def get_rendered_wikipedia_article(self, request):
        items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
        article_name = list(items['wikipediaArticleName'].keys())[0]
        #wikipedia_article = WikipediaAPIHandler().get_wikipedia_article(article_name)
        wikipedia_article = DataRepoHandler().get_wikipedia_article(article_name)
        line_dict, identifier_line_dict, processed_file = WikipediaParser(wikipedia_article, article_name).process()
        dicts = {'identifiers': identifier_line_dict, 'lines': line_dict}

        self.dicts_to_cache(dicts)

        print('start screen view: get_rendered_wikipedia_article')
        #print(processed_file)

        #return render(request,
        #              #'annotation_template.html',
        #              '/annotation/',
        #              {'File': processed_file})

        return redirect('/')


    def get_repo_content(self):
        """
        Get the repo content for the datarepo/annotation folder, i.e. all files that have been annotated in the past.
        :return:
        """
        file_names = DataRepoHandler().list_directory()
        return HttpResponse(
                            json.dumps({'fileNames': file_names}),
                            content_type='application/json'
        )


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
            return self.get_rendered_wikipedia_article(request)

        elif 'getRepoContent' in request.POST:
            print('getRepoContent')
            return self.get_repo_content()


        print('before bottom return')
        return render(request, "file_upload_wiki_suggestions_2.html", self.initial)

