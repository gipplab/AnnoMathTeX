import os
import urllib3
urllib3.disable_warnings()
from github import Github, GithubException



class DataRepoHandler:

    def __init__(self, token=os.getenv('apikey', False)):
        self.token = token

        #uncomment for local testing
        if not token:
            from .key import local_token
            self.token = local_token

        #uncomment for wmflabs
        #if not token:
        #    print('Token not set')
        #    exit(2)


        self.g = Github(self.token)
        self.repo = self.g.get_repo("ag-gipp/dataAnnoMathTex")
        self.user = self.g.get_user()

    def commit_file(self, file_name, file_content):
        print('committing file {}'.format(file_name))
        try:
            self.repo.create_file(file_name, "commiting file {}".format(file_name), file_content)
        except GithubException as e:
            print(e)
            contents = self.repo.get_contents(file_name)
            self.repo.update_file(file_name, "updating file {}".format(file_name), file_content, contents.sha)
        except AttributeError as e:
            print(e)
        return

    def delete_file(self, file_name):
        contents = self.repo.get_contents(file_name)
        self.repo.delete_file(file_name, "Deleting file {}".format(file_name), contents.sha)
        return

    def commit_formula_concepts(self, annotations):
        pass



class FormulaConceptHandler:

    def __init__(self, annotations):
        self.annotations = annotations

    def get_formulae(self):
        print(self.annotations)



if __name__ == '__main__':
    from key import local_token
    d = DataRepoHandler(local_token)
    #d.delete_file('sun.csv')






