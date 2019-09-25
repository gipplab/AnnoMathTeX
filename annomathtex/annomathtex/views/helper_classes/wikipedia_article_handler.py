from jquery_unparam import jquery_unparam
from ...parsing.wikipedia_parser import WikipediaParser
from ...views.helper_classes.data_repo_handler import DataRepoHandler
from ...views.helper_classes.cache_handler import CacheHandler
from ...views.helper_classes.wikipedia_api_handler import WikipediaAPIHandler

from django.shortcuts import render, redirect


class WikipediaArticleHandler:

    def __init__(self, request, items):
        self.request = request
        self.items = items


    def get_rendered_wikipedia_article(self):
        article_name = list(self.items['wikipediaArticleName'].keys())[0]
        wikipedia_article = DataRepoHandler().get_wikipedia_article(article_name)
        line_dict, identifier_line_dict, processed_file = WikipediaParser(wikipedia_article, article_name).process()
        dicts = {'identifiers': identifier_line_dict, 'lines': line_dict}
        CacheHandler().dicts_to_cache(dicts)
        return redirect('/', {'File': processed_file, 'test': 2})

    def add_wikipedia_article(self, template_name, form):
        article_name = list(self.items['wikipediaArticleName'].keys())[0]
        w = WikipediaAPIHandler()
        article = w.get_wikipedia_article(article_name)
        DataRepoHandler().add_wikipedia_article_to_repo(article, article_name)
        return render(self.request, template_name, {'form': form})
