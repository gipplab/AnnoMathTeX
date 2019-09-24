import json

from django.http import HttpResponse
from jquery_unparam import jquery_unparam

from ...views.helper_classes.wikipedia_api_handler import WikipediaAPIHandler


class WikipediaQueryHandler:

    def __init__(self, request):
        self.request = request


    def get_suggestions(self):
        items = {k: jquery_unparam(v) for (k, v) in self.request.POST.items()}
        search_string = list(items['wikipediaSubmit'].keys())[0]
        w = WikipediaAPIHandler()
        r = w.get_suggestions(search_string)
        return HttpResponse(
                            json.dumps({'wikipediaResults': r}),
                            content_type='application/json')
