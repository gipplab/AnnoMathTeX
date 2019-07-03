from ..views.data_repo_handler import DataRepoHandler



class FormulaConceptDBHandler(object):

    def fetch_formula_concept_db(self):
        data_repo_handler = DataRepoHandler()
        formula_concepts = data_repo_handler.get_formula_concepts()
        return formula_concepts


    def query_texstrings(self):
        pass


    def query_identifiers(self):
        pass



