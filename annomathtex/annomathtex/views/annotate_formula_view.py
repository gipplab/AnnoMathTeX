import json
import logging


from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from jquery_unparam import jquery_unparam
from ..forms.uploadfileform import UploadFileForm
from ..forms.save_annotation_form import SaveAnnotationForm

from ..views.eval_file_writer import EvalFileWriter
from ..views.data_repo_handler import DataRepoHandler, FormulaConceptHandler, ManualRecommendationsCleaner
from .helper_functions import handle_annotations
from ..config import *

from .helper_classes.token_clicked_handler import TokenClickedHandler
from .helper_classes.file_handler import FileHandler
from .helper_classes.cache_handler import CacheHandler
from .helper_classes.wikipedia_query_handler import WikipediaQueryHandler
from .helper_classes.wikipedia_article_name_handler import WikipediaArticleNameHandler
from .helper_classes.repo_content_handler import RepoContentHandler
from .helper_classes.session_saved_handler import SessionSavedHandler


logging.basicConfig(level=logging.INFO)
__LOGGER__ = logging.getLogger(__name__)


class FileUploadView(View):
    """
    This view is where everything going on in the frontend is handled.
    """
    form_class = UploadFileForm
    initial = {'key': 'value'}
    save_annotation_form = {'form': SaveAnnotationForm()}
    template_name = 'annotation_template_tmp.html'


    def get(self, request, *args, **kwargs):
        """
        This method handles get request from the frontend.
        :param request: Request object. Request made by the user through the frontend.
        :return: The rendered response containing the template name and the necessary form.
        """
        article_name = CacheHandler().read_file_name_cache()
        processed_file = FileHandler(request).get_processed_wikipedia_article(article_name)
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
        #items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
        #print(items)

        if 'file_submit' in request.POST:
            return FileHandler(request).process_local_file()

        elif 'queryDict' in request.POST:
            print('queryDict')
            return TokenClickedHandler(request).get_recommendations()

        elif 'annotations' in request.POST:
            print('annotations')
            return SessionSavedHandler(request).save()

        #todo: check if not used
        elif 'wikipediaSubmit' in request.POST:
            print("WIKIPEDIA SUBMIT")
            return WikipediaQueryHandler(request).get_suggestions()

        elif 'wikipediaArticleName' in request.POST:
            print('wikipediaArticleName')
            return WikipediaArticleNameHandler(request).handle_name()

        elif 'getRepoContent' in request.POST:
            print('getRepoContent')
            return RepoContentHandler().get_repo_content()



        return render(request, "file_upload_wiki_suggestions_2.html", self.initial)
