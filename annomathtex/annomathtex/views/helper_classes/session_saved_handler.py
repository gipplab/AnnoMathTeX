import json
import logging
from django.http import HttpResponse
from .data_repo_handler import DataRepoHandler, ManualRecommendationsCleaner
from .helper_functions import handle_annotations
from .eval_file_writer import EvalFileWriter
from .formula_concept_handler import FormulaConceptHandler

from ...config import *


logging.basicConfig(level=logging.INFO)
session_saved_handler_logger = logging.getLogger(__name__)

class SessionSavedHandler:
    """
    This class receives data from the frontend, when the user mouse clicks the "save" button.

    Annotated items: e.g. the user annotated the identifier "E" with the wikidata item "energy (Q11379)".
    Marked items: A word that wasn't found by the named entity tagger, but the user decided it should have been.
    Unmarked items: A Word that was found by the named entity tagger, but the user decided it shouldn't have been.

    :param request: Request object. Request made by the user through the frontend.
    :return: The rendered response containing the template name and the necessary form.
    """


    #NOTE: in earlier version, annotations was used instead of cleaned_annotations, I think this was a mistake
    #      but haven't tested yet

    def __init__(self, request, items):
        self.request = request
        self.items = items


    def add_qids(self, manual_recommendations):
        # not necessary???
        # if the wikidata item wasn't found based on the name, it won't be found now
        pass


    def formula_concept_db_initial_commit(self, annotations):
        """
        :param annotations:
        :return:
        """
        formulae = FormulaConceptHandler(annotations).get_formulae()
        DataRepoHandler().commit_file('sources/formula_concepts.txt', json.dumps(formulae))

    def post_process_annotations(self, annotations):

        def apostroph(item):
            return item['name'].replace('__APOSTROPH__', '\'').replace('&', '')
        if 'global' in annotations:
            for symbol in annotations['global']:
                item = annotations['global'][symbol]
                item['name'] = apostroph(item)

        if 'local' in annotations:
            for symbol in annotations['local']:
                for id in annotations['local'][symbol]:
                    item = annotations['local'][symbol][id]
                    item['name'] = apostroph(item)

        return annotations

    def save(self):
        annotations = self.post_process_annotations(self.items['annotations'])
        file_name = self.items['fileName']['f']

        #file_name = file_name.replace(' (Wikitext)', '.txt')
        #file_name = file_name.replace(' (LaTeX)', '.tex')

        file_name = file_name.replace(' (Wikitext)', '')
        file_name = file_name.replace(' (LaTeX)', '')


        session_saved_handler_logger.info(file_name)



        #session_saved_handler_logger.info(self.items['annotations'])

        manual_recommendations = self.items['manualRecommendations']

        m = ManualRecommendationsCleaner(manual_recommendations)
        cleaned_manual_recommendations = m.get_recommendations()


        cleaned_annotations = handle_annotations(annotations)
        #session_saved_handler_logger.info(cleaned_annotations)


        #self.formula_concept_db_initial_commit(annotations)
        #self.save_files_locally(file_name, cleaned_annotations)



        self.save_files_to_repo(file_name, cleaned_annotations, cleaned_manual_recommendations)

        return HttpResponse(
            json.dumps({'testkey': 'testvalue'}),
            content_type='application/json'
        )


    def save_files_locally(self, file_name, cleaned_annotations):
        annotation_file_path = create_annotation_file_path(file_name)
        with open(annotation_file_path, 'w') as f:
            #__LOGGER__.debug(' WRITING TO FILE {}'.format(annotation_file_path))
            json.dump(cleaned_annotations, f)



    def save_files_to_repo(self, file_name, cleaned_annotations, cleaned_manual_recommendations):


        data_repo_handler = DataRepoHandler()
        data_repo_handler.commit_manual_recommendations(cleaned_manual_recommendations)
        data_repo_handler.commit_formula_concepts(cleaned_annotations)
        annotation_file_name = create_annotation_file_name(file_name)
        data_repo_handler.commit_annotations(annotation_file_name, json.dumps(cleaned_annotations))
        eval_file_writer = EvalFileWriter(cleaned_annotations, file_name)
        evaluation_csv_string = eval_file_writer.get_csv_for_repo()
        evaluation_file_name = create_evaluation_file_name(file_name)
        data_repo_handler.commit_evaluation(evaluation_file_name, evaluation_csv_string)
        return

