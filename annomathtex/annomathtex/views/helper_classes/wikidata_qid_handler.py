import json
import logging
from django.http import HttpResponse
from .data_repo_handler import DataRepoHandler


from ...config import *


logging.basicConfig(level=logging.INFO)
wikidata_qid_handler_logger = logging.getLogger(__name__)

class WikidataQIDHandler:


    def __init__(self, request, items):
        self.request = request
        self.items = items


    def add_qids(self):
        name = list(self.items['name'].keys())[0]
        is_formula_str = list(self.items['isFormula'].keys())[0]
        is_formula = True if is_formula_str == 'true' else False
        wikidata_qid_handler_logger.info('get qid for: {}'.format(name))
        #wikidata_qid_handler_logger.info(self.items)
        d = DataRepoHandler()


        source = d.get_wikidata_formulae() if is_formula else d.get_wikidata_identifiers_by_name()
        if name in source:
            qid = source[name]['qid']
        else:
            qid = 'N/A'


        return HttpResponse(
            json.dumps({'qid': qid, 'name': name}),
            content_type='application/json'
        )


