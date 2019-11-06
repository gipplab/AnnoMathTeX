import logging
from django.shortcuts import render
from django.views.generic import View
from jquery_unparam import jquery_unparam

from ..forms.testform import TestForm
from ..forms.uploadfileform import UploadFileForm
from .helper_classes.repo_content_handler import RepoContentHandler
from .helper_classes.wikipedia_query_handler import WikipediaQueryHandler
from .helper_classes.wikipedia_article_handler import WikipediaArticleHandler
from .helper_classes.wikidata_qid_handler import WikidataQIDHandler

logging.basicConfig(level=logging.INFO)
start_screen_view_logger = logging.getLogger(__name__)

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
        start_screen_view_logger.info('GET, template_name: {}'.format(self.template_name))
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
        items = {k: jquery_unparam(v) for (k, v) in self.request.POST.items()}
        action = list(items['action'].keys())[0]

        start_screen_view_logger.info('POST, action: {}'.format(action))
        start_screen_view_logger.info(items)

        if action == 'getRepoContent':
            return RepoContentHandler(items).get_repo_content()

        elif action == 'deleteFileFromRepo':
            return RepoContentHandler(items).move_file_to_archive()

        elif action == 'getWikipediaSuggestions':
            return WikipediaQueryHandler(request, items).get_suggestions()

        elif action == 'addArticleToRepo':
            return WikipediaArticleHandler(request, items).add_wikipedia_article(self.template_name, TestForm())

        elif action == 'checkManualRecommendationQID':
            response = WikidataQIDHandler(request, items).add_qids()
            return response

        return render(request, "file_upload_wiki_suggestions_2.html", self.initial)

