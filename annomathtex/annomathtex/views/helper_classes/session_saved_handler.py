import json
from jquery_unparam import jquery_unparam
from django.http import HttpResponse
from ...views.helper_classes.data_repo_handler import DataRepoHandler, ManualRecommendationsCleaner
from ...views.helper_classes.helper_functions import handle_annotations
from ...views.helper_classes.eval_file_writer import EvalFileWriter

from ...config import *

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


    def __init__(self, request):
        self.request = request



    def save(self):
        items = {k: jquery_unparam(v) for (k, v) in self.request.POST.items()}
        annotations = items['annotations']
        file_name = items['fileName']['f']
        manual_recommendations = items['manualRecommendations']

        m = ManualRecommendationsCleaner(manual_recommendations)
        cleaned_manual_recommendations = m.get_recommendations()
        cleaned_annotations = handle_annotations(annotations)

        #self.save_files_locally(file_name, cleaned_annotations)
        #self.save_files_to_repo(file_name, cleaned_annotations, cleaned_manual_recommendations)

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

