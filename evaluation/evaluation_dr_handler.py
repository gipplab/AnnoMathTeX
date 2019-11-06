from github import Github, GithubException
import json
import re
import csv


class EvaluationDRHandler:


    def __init__(self):
        from key import local_token
        self.token = local_token
        self.g = Github(self.token)
        self.repo = self.g.get_repo("ag-gipp/dataAnnoMathTeX")
        self.user = self.g.get_user()



    def commit_file(self, file_name, file_content):
        try:
            self.repo.create_file(file_name, "commiting file {}".format(file_name), file_content)
        except GithubException as e:
            #data_repo_handler_logger.info(e)
            contents = self.repo.get_contents(file_name)
            self.repo.update_file(file_name, "updating file {}".format(file_name), file_content, contents.sha)
            #data_repo_handler_logger.info("updating file {}".format(file_name))
        except AttributeError as e:
            pass
            #data_repo_handler_logger.info(e)

        return

    def delete_file(self, file_name):
        contents = self.repo.get_contents(file_name)
        self.repo.delete_file(file_name, "Deleting file {}".format(file_name), contents.sha)
        return



    def list_directory(self, dirname='evaluation'):
        dir_contents = self.repo.get_dir_contents(dirname)

        def clean_name(content_file):
            regex = r'(?<={}/).*?(?=\"\))'.format(dirname)
            file_name = re.search(regex, str(content_file))
            file_name = file_name.group()
            #file_name = file_name.replace('_', ' ')
            return file_name

        file_names = list(map(clean_name, dir_contents))
        return file_names

    def get_file(self, path):
        encoded_content = self.repo.get_file_contents(path)
        decoded_content = encoded_content.decoded_content
        return decoded_content.decode('utf-8')
        #print(decoded_content)
        #formula_concepts = json.loads(decoded_content)
        #return formula_concepts


    def get_all_evaluation_files(self, ignorelist=[]):
        eval_file_names = self.list_directory()
        all_eval_files = []
        for file_name in eval_file_names:

            if file_name not in ignorelist:
                file_string = self.get_file('evaluation/{}'.format(file_name))
                file_list = file_string.split('\n')
                file_csv = csv.reader(file_list)
                file = list(file_csv)
                all_eval_files.append(file)

        return all_eval_files


    def get_all_annotation_files(self, ignorelist=[]):
        annotation_file_names = self.list_directory('annotation')
        all_eval_files = []
        for file_name in annotation_file_names:
            if file_name not in ignorelist:
                str_content = self.get_file('annotation/{}'.format(file_name))
                annotation_dict = json.loads(str_content)
                all_eval_files.append(annotation_dict)

        return all_eval_files



if __name__ == '__main__':
    EvaluationDRHandler().get_all_evaluation_files()
