from django.shortcuts import render
from jquery_unparam import jquery_unparam

from ...views.helper_classes.cache_handler import CacheHandler

class WikipediaArticleNameHandler:

    def __init__(self, request, items):
        self.request = request
        self.items = items
        self.initial = {'key': 'value'}

    def handle_name(self):
        article_name = list(self.items['wikipediaArticleName'].keys())[0]
        CacheHandler().write_file_name_cache(article_name)
        return render(self.request, "annotation_template_tmp.html", self.initial)
