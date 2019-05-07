import csv
import os
from ..config import evaluations_path, evaluation_annotations_path


class EvalFileWriter:

    def __init__(self, annotations):
        self.loc = annotations['local']
        self.glob = annotations['global']



    def fill_remaining(self, sources_with_nums):
        sources = ['ArXiV', 'Wikipedia', 'Wikidata', 'WordWindow']
        completed_list = []
        for source in sources:
            if source in sources_with_nums:
                completed_list.append(sources_with_nums[source])
            else:
                completed_list.append('-')

        return completed_list


    def handle_local(self):
        rows = []
        for token_content in self.loc:
            for id in self.loc[token_content]:
                sources_with_nums = self.fill_remaining(self.loc[token_content][id]['sourcesWithNums'])
                row = [token_content, self.loc[token_content][id]['name']] + sources_with_nums + ['local']
                rows.append(row)

        return rows


    def handle_global(self):
        rows = []
        for token_content in self.glob:
            sources_with_nums = self.fill_remaining(self.glob[token_content]['sourcesWithNums'])
            row = [token_content, self.glob[token_content]['name']] + sources_with_nums + ['global']
            rows.append(row)

        return rows


    def write(self):
        all_rows = self.handle_local() + self.handle_global()

        if evaluations_path in os.listdir(evaluation_annotations_path):
            with open(evaluations_path, 'a') as f:
                f.write(all_rows)
        else:
            header = ['Identifier', 'Name', 'ArXiV', 'Wikipedia', 'Wikidata', 'WordWindow', 'global/local']
            with open(evaluations_path, 'w') as f:
                csv_writer = csv.writer(f, delimiter=',')
                csv_writer.writerow(header)
                for row in all_rows:
                    csv_writer.writerow(row)



