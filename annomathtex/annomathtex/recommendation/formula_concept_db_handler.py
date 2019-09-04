from ..views.data_repo_handler import DataRepoHandler
from fuzzywuzzy import fuzz


class FormulaConceptDBHandler(object):

    def __init__(self):
        self.formula_concepts = DataRepoHandler().get_formula_concepts()

    def fetch_formula_concept_db(self):
        data_repo_handler = DataRepoHandler()
        formula_concepts = data_repo_handler.get_formula_concepts()
        return formula_concepts


    def query_tex_string(self, tex_string_1, threshold=65):
        recommendations = []
        for fc in self.formula_concepts:

            tex_strings = self.formula_concepts[fc]['TeXStrings']
            for tex_string_2 in tex_strings:
                if fuzz.token_sort_ratio(tex_string_1, tex_string_2) >= threshold:
                    recommendations.append({'name': fc})

        return recommendations[:10]



        """formula_concept_names = list(formula_concepts.keys())
        print(formula_concepts)
        if tex_string in formula_concept_names:
            formula = formula_concepts[tex_string]
            existing_tex_strings = formula['TeXSTrings']
            #identifiers = formula['Identifiers']"""



    def query_identifiers(self):
        pass




if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from views.data_repo_handler import DataRepoHandler
    f = FormulaConceptDBHandler()
    c = f.query_tex_string('E = m c^2')
    print(c)
