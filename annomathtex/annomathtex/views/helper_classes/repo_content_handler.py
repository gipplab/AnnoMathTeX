import json
import logging
from django.http import HttpResponse
from .data_repo_handler import DataRepoHandler
from ...config import *

logging.basicConfig(level=logging.INFO)
repo_content_handler_logger = logging.getLogger(__name__)


class RepoContentHandler:

    def __init__(self, items):
        self.items = items
        self.data_repo_handler = DataRepoHandler()

    def get_repo_content(self):
        """
        Get the repo content for the datarepo/annotation folder, i.e. all files that have been annotated in the past.
        :return:
        """
        file_names = self.data_repo_handler.list_directory()#DataRepoHandler().list_directory()
        return HttpResponse(
                            json.dumps({'fileNames': file_names}),
                            content_type='application/json'
        )


    def move_file_to_archive(self):
        file_name = list(self.items['fileName'].keys())[0]
        file_name = create_annotation_file_name(file_name) #file_name.replace('\s', '_') + '.txt'
        annotation_file_name = file_name
        evaluation_file_name = create_evaluation_file_name(file_name)

        repo_content_handler_logger.info(file_name)
        #move to archive folder
        self.data_repo_handler.rename_file('files/{}'.format(file_name), 'archive/files/{}'.format(file_name))
        try:
            self.data_repo_handler.rename_file('annotation/{}'.format(annotation_file_name),
                                               'archive/annotation/{}'.format(annotation_file_name))
            self.data_repo_handler.rename_file('evaluation/{}'.format(evaluation_file_name),
                                               'archive/evaluation/{}'.format(evaluation_file_name))

        except Exception as e:
            repo_content_handler_logger.info(e)




        return self.get_repo_content()
