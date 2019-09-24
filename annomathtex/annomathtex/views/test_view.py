import pickle

from django.shortcuts import render
from django.views.generic import View
from jquery_unparam import jquery_unparam

from ..views.helper_classes.data_repo_handler import DataRepoHandler
from ..parsing.wikipedia_parser import WikipediaParser

from ..forms.uploadfileform import UploadFileForm


from ..config import *



class TestView(View):

    form_class = UploadFileForm
    initial = {'key': 'value'}
    template_name = 'test_template.html'
    path = os.path.join(os.getcwd(), 'annomathtex', 'views', 'cache', 'file_name_cache.txt')

    def read_file_name_cache(self):
        with open(self.path, 'r') as infile:
            file_name = infile.read()
        return file_name

    def write_file_name_cache(self, file_name):
        with open(self.path, 'w') as outfile:
            outfile.truncate(0)
            outfile.write(file_name)
        return

    def dicts_to_cache(self, dicts):
        """
        Write the dictionary, that is used to form the word window when the user clicks a token, to the cache.
        :param dicts: Line dictionary and identifier line dictionary.
        :return: None; files are pickled and stored in cache.
        """
        path = view_cache_path + 'dicts'
        with open(path, 'wb') as outfile:
            pickle.dump(dicts, outfile)

    def get_rendered_wikipedia_article(self, article_name):
        wikipedia_article = DataRepoHandler().get_wikipedia_article(article_name)
        line_dict, identifier_line_dict, processed_file = WikipediaParser(wikipedia_article, article_name).process()
        dicts = {'identifiers': identifier_line_dict, 'lines': line_dict}

        self.dicts_to_cache(dicts)

        return processed_file


    def get(self, request, *args, **kwargs):
        """
        This method handles get request from the frontend.
        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name and the necessary form.
        """
        #form = TestForm()
        article_name = self.read_file_name_cache()
        print('file_name: {}'.format(article_name))
        processed_file = self.get_rendered_wikipedia_article(article_name)
        return render(request, self.template_name, {'File': processed_file, 'test': 3})


    def post(self, request, *args, **kwargs):
        """
        This method handles post request from the frontend. Any data being passed to the backend will be passed through
        a post request, meaning that this method will be called for all tasks that require the frontend in any way to
        access the backend.
        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name, the necessary form and the response data (if
                 applicable).
        """
        items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
        article_name = list(items['wikipediaArticleName'].keys())[0]
        self.write_file_name_cache(article_name)
        return render(request, "test_template.html", self.initial)

