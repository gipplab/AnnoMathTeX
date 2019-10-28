import csv
import os
from io import StringIO
from ...config import evaluation_annotations_path, create_evaluation_file_path, create_evaluation_file_name


class EvalFileWriter:
    """
    This class is used to write the evaluation results from the annotations as a table to a csv file.
    This table is of the form:

    Identifier | Name | ArXiV | Wikipedia | Wikidata | WordWindow | global/local

    S          | set  |   1   |     -     |     -    |      4     |   global



    New Table:

        Identifier | Name | ArXiV | Wikipedia | Wikidata | Wikidata1 | Wikidata2 | WordWindow | FormulaConceptDB | global/local

        S          | set  |   1   |     -     |    -     | -     |      -    |      4     |        -         | global


    ArXiV and Wikipedia, Wikidata  are exclusive to identifiers
    Wikidata1 Wikidata2 and FormulaConceptDB are exclusive to formulae


    In the above example, the identifier "S" was annotated with the concept "set". The concept "set" appeared in the
    recommendations from the ArXiV column (position 1) and the WordWindow column (position 4). The other sources did
    not list it. Furthermore, the identifier was annotated globally with this concept.
    """

    def __init__(self, annotations, file_name=None):
        self.loc = annotations['local'] if 'local' in annotations else {}
        self.glob = annotations['global'] if 'global' in annotations else {}

        self.file_name = file_name



    def fill_remaining(self, sources_with_nums):
        """
        The sources that did not list the chosen recommendation are filled with a dash '-'.
        :param sources_with_nums: A dictionary containing the sources and the position of the recommendation (if
        present) in the column. For the above example: {'ArXiv': 1, 'WordWindow': 4}.
        :return: Completed dictionary; for the above example:
        {'ArXiv': 1, 'Wikipedia': '-', 'Wikidata': '-',  'WordWindow': 4}
        """
        #sources = ['ArXiv', 'Wikipedia', 'Wikidata', 'WordWindow']
        sources = ['ArXiv', 'Wikipedia', 'Wikidata', 'Wikidata1', 'Wikidata2', 'WordWindow', 'FormulaConceptDB']
        completed_list = []
        for source in sources:
            if source in sources_with_nums:
                completed_list.append(sources_with_nums[source])
            else:
                completed_list.append('-')

        return completed_list


    def handle_local(self):
        """
        The local annotations are handled in this method, i.e. transformed into rows for the csv file.
        :return: All the rows of local annotations.
        """
        rows = []
        for token_content in self.loc:
            for id in self.loc[token_content]:
                sources_with_nums = self.fill_remaining(self.loc[token_content][id]['sourcesWithNums'])
                row = [token_content, self.loc[token_content][id]['name']] + \
                      sources_with_nums + \
                      ['local'] + \
                      [self.loc[token_content][id]['time'],  self.loc[token_content][id]['time']]
                rows.append(row)

        return rows


    def handle_global(self):
        """
        The global annotations are handled in this method, i.e. transformed into rows for the csv file.
        :return: All the rows of global annotations.
        """
        rows = []
        for token_content in self.glob:
            #print(self.glob[token_content])
            try:
                sources_with_nums = self.fill_remaining(self.glob[token_content]['sourcesWithNums'])
            except Exception:
                sources_with_nums = self.fill_remaining({})

            row = [token_content, self.glob[token_content]['name']] + \
                  sources_with_nums + ['global'] + \
                  [self.glob[token_content]['time'], self.glob[token_content]['manualSelectionTime']]
            rows.append(row)


        return rows


    def write(self):
        """
        Write the processed rows to a csv file.
        :return: None.
        """
        all_rows = self.handle_local() + self.handle_global()
        evaluation_file_name = create_evaluation_file_name(self.file_name)
        evaluation_file_path = create_evaluation_file_path(self.file_name)


        #currently only overwriting
        """if evaluation_file_name in os.listdir(evaluation_annotations_path):
            with open(evaluation_file_path, 'a') as f:
                f.write(all_rows)
        else:
            header = ['Identifier', 'Name', 'ArXiV', 'Wikipedia', 'Wikidata', 'WordWindow', 'type', 'time']
            with open(evaluation_file_path, 'w') as f:
                csv_writer = csv.writer(f, delimiter=',')
                csv_writer.writerow(header)
                for row in all_rows:
                    csv_writer.writerow(row)"""

        header = ['Identifier / Formula',
                  'Name',
                  'ArXiV', 'Wikipedia', 'Wikidata', 'WordWindow',
                  'type', 'time', 'manualSelectionTime']
        with open(evaluation_file_path, 'w') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(header)
            for row in all_rows:
                csv_writer.writerow(row)


    def get_csv_for_repo(self):
        """
        Create a csv file of the evaluation as a string for adding to the github repository ("ag-gipp/dataAnnoMathTex")
        :return: csv as string
        """
        all_rows = self.handle_local() + self.handle_global()
        f = StringIO()
        #header = ['Identifier / Formula', 'Name', 'ArXiV', 'Wikipedia', 'Wikidata', 'WordWindow', 'type']
        header = ['Identifier / Formula',
                  'Name',
                  'ArXiV', 'Wikipedia', 'Wikidata', 'Wikidata1', 'Wikidata2',  'WordWindow', 'FormulaConceptDB',
                  'type',
                  'time', 'manualSelectionTime']
        csv.writer(f).writerows([header] + all_rows)
        return f.getvalue()




