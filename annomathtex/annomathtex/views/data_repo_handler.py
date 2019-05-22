import os
import urllib3
urllib3.disable_warnings()
from github import Github, GithubException



class DataRepoHandler:

    def __init__(self, token=os.getenv('apikey', False)):
        self.token = token

        if not token:
            #from .key import local_token
            #self.token = local_token
            print('token not set')

        self.g = Github(self.token)
        self.repo = self.g.get_repo("ag-gipp/dataAnnoMathTex")
        self.user = self.g.get_user()

    def commit_file(self, file_name, file_content):
        try:
            self.repo.create_file(file_name, "commiting file {}".format(file_name), file_content)
        except GithubException as e:
            #print(e)
            contents = self.repo.get_contents(file_name)
            self.repo.update_file(file_name, "updating file {}".format(file_name), file_content, contents.sha)
        return

    def delete_file(self, file_name):
        contents = self.repo.get_contents(file_name)
        self.repo.delete_file(file_name, "Deleting file {}".format(file_name), contents.sha)
        return



if __name__ == '__main__':
    from key import local_token
    d = DataRepoHandler(local_token)
    d.delete_file('sun.csv')






