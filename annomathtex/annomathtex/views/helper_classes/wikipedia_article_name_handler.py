from django.shortcuts import render
from jquery_unparam import jquery_unparam

from ...views.helper_classes.cache_handler import CacheHandler

class WikipediaArticleNameHandler:

    def __init__(self, request):
        self.request = request
        self.initial = {'key': 'value'}

    def handle_name(self):
        items = {k: jquery_unparam(v) for (k, v) in self.request.POST.items()}
        article_name = list(items['wikipediaArticleName'].keys())[0]
        CacheHandler().write_file_name_cache(article_name)
        return render(self.request, "annotation_template_tmp.html", self.initial)
