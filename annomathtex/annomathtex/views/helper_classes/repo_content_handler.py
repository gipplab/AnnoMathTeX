import json
from django.http import HttpResponse
from ...views.data_repo_handler import DataRepoHandler


class RepoContentHandler:

    def get_repo_content(self):
        """
        Get the repo content for the datarepo/annotation folder, i.e. all files that have been annotated in the past.
        :return:
        """
        file_names = DataRepoHandler().list_directory()
        return HttpResponse(
                            json.dumps({'fileNames': file_names}),
                            content_type='application/json'
        )
