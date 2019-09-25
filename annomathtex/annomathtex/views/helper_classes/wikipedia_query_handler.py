import json

from django.http import HttpResponse

from ...views.helper_classes.wikipedia_api_handler import WikipediaAPIHandler


class WikipediaQueryHandler:

    def __init__(self, request, items):
        self.request = request
        self.items = items


    def get_suggestions(self):
        search_string = list(self.items['searchString'].keys())[0]
        w = WikipediaAPIHandler()
        r = w.get_suggestions(search_string)
        return HttpResponse(
                            json.dumps({'wikipediaResults': r}),
                            content_type='application/json')
