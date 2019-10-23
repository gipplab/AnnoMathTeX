import logging


logging.basicConfig(level=logging.DEBUG)
formula_concept_handler_logger = logging.getLogger(__name__)

class FormulaConceptHandler:
    """
    Prepares the formulae for adding to the formula concepts file.
    """

    def __init__(self, annotations):
        self.annotations = annotations

    def extract_formulae(self):
        formulae = {}

        if 'global' in self.annotations:
            g = self.annotations['global']
            for key in g:
                instance = g[key]
                formula_concept_handler_logger.info('INSTANCE: {}'.format(instance))
                try:
                    if instance['type'] == 'Formula':
                        formulae[key.replace('__EQUALS__', '=')] = {
                            'name': instance['name'].replace('__EQUALS__', '='),
                            'qid': instance['qid']
                            #'sourcesWithNums': instance['sourcesWithNums']
                        }
                except:
                    formula_concept_handler_logger.info(instance)

        if 'local' in self.annotations:
            l = self.annotations['local']
            for key in l:
                for unique_id in l[key]:
                    instance = l[key][unique_id]
                    if instance['type'] == 'Formula':
                        formulae[key.replace('__EQUALS__', '=')] = {
                            'name': instance['name'].replace('__EQUALS__', '='),
                            'qid': instance['qid']
                            #'sourcesWithNums': instance['sourcesWithNums']
                        }

        return formulae

    #todo: simplify
    def add_identifiers(self):
        formulae = self.extract_formulae()
        formula_concept_handler_logger.info(formulae)
        if 'global' in self.annotations:
            g = self.annotations['global']
            for key in g:
                instance = g[key]
                formula_concept_handler_logger.info(instance)
                m = instance['mathEnv']
                is_identifier = True if instance['type'] == 'Identifier' else False
                if m in formulae and is_identifier:
                    if 'identifiers' in formulae[m]:
                        #formulae[m]['identifiers'][key] = instance['name']
                        formulae[m]['identifiers'][key] = {'name': instance['name'], 'qid': instance['qid']}

                    else:
                        #formulae[m]['identifiers'] = {key: instance['name']}
                        formulae[m]['identifiers'] = {key: {'name': instance['name'], 'qid': instance['qid']}}

        if 'local' in self.annotations:
            l = self.annotations['local']
            for key in l:
                for unique_id in l[key]:
                    instance = l[key][unique_id]
                    m = instance['mathEnv']
                    is_identifier = True if instance['type'] == 'Identifier' else False
                    if m in formulae and is_identifier:
                        if 'identifiers' in formulae[m]:
                            #formulae[m]['identifiers'][key] = instance['name']
                            formulae[m]['identifiers'][key] = {'name': instance['name'], 'qid': instance['qid']}
                        else:
                            #formulae[m]['identifiers'] = {key: instance['name']}
                            formulae[m]['identifiers'] = {key: {'name': instance['name'], 'qid': instance['qid']} }
        return formulae


    def get_formulae(self):
        formulae = self.add_identifiers()
        reversed_formulae = {}

        for formula_string in formulae:
            name = formulae[formula_string]['name']
            identifiers = formulae[formula_string]['identifiers']
            qid = formulae[formula_string]['qid']
            reversed_formulae[name] = {'TeXStrings': [formula_string],
                                       'Identifiers': identifiers,
                                       'qid': qid}

        return reversed_formulae
