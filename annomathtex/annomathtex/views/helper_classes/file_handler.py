import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from jquery_unparam import jquery_unparam


from ...forms.uploadfileform import UploadFileForm
from ...forms.save_annotation_form import SaveAnnotationForm

from ...views.helper_classes.cache_handler import CacheHandler
from ...views.data_repo_handler import DataRepoHandler

from ...parsing.txt_parser import TXTParser
from ...parsing.tex_parser import TEXParser
from ...parsing.wikipedia_parser import WikipediaParser


class FileHandler:
    """
    In this class the user selected file is checked for the type of the file (txt, tex, html,...) and the
    appropriate parser for the file type is selected. After the file is processed by the parser it is returned to
    the frontend for rendering.

    The dictionaries line_dict and identifier_line_dict are needed for the creation of the word window
    surrounding a token (it is constructed when the user mouse clicks a token (identifier or formula).

    line_dict is a dictionary of line numbers as keys and a list of the named entities that appear on the

    identifier_line_dict is a dictionary of the unique ids of identifiers as keys and the line number they
    appear on as values.

    :param request: Request object; request made by the user through the frontend.
    :return: The rendered response to the frontend.
    """

    def __init__(self, request):
        print('FILEHANDLER')
        self.request = request
        self.save_annotation_form = {'form': SaveAnnotationForm()}


    def get_processed_wikipedia_article(self, article_name):
        wikipedia_article = DataRepoHandler().get_wikipedia_article(article_name)
        line_dict, identifier_line_dict, processed_file = WikipediaParser(wikipedia_article, article_name).process()
        dicts = {'identifiers': identifier_line_dict, 'lines': line_dict}

        CacheHandler().dicts_to_cache(dicts)

        return processed_file


    def process_local_file(self):

        form = UploadFileForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            request_file = self.request.FILES['file']
            file_name = str(request_file)
            if file_name.endswith('.tex'):
                line_dict, identifier_line_dict, processed_file = TEXParser(request_file, file_name).process()
            elif file_name.endswith('.txt'):
                line_dict, identifier_line_dict, processed_file = TXTParser(request_file, file_name).process()
            else:
                line_dict, identifier_line_dict, processed_file = None, None, None


            dicts = {'identifiers': identifier_line_dict, 'lines': line_dict}

            CacheHandler.dicts_to_cache(dicts)


            return render(self.request,
                          #'annotation_template.html',
                          'annotation_template_tmp.html',
                          {'File': processed_file})


        return render(self.request, "render_file_template.html", self.save_annotation_form)
