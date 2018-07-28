#import latex2sympy
from latex2sympy.process_latex import process_sympy
from sympy.core.sympify import sympify
from sympy import Symbol

from JsonConvert import JsonConvert, Formulae, Formula, Identifiers, Identifier

def process_formulae(formulae, formulae_json):

    #for each formula
    for formula in formulae:

        print("Formula Expression: " + formula)

        #formula annotation recommendation
        formula_feedback = "i"
        for formula_iter in formulae_json.Formulae:
            if formula_iter.Expression==formula:
                formula_feedback = input("Formula Name: " + formula_iter.Name + " y=yes/n=no/i=input?")
                if formula_feedback=="y" or formula_feedback=="i":
                    break
                    #TODO: do not break for all formulae, but jump to the next formula!

        #ask for formula name and QID
        if formula_feedback == "y":
            formula_name = formula_iter.Name
            formula_qid = formula_iter.WikiQID
            break
        else:
            formula_name = input("Formula Name: ")
            formula_qid = input("Formula QID: ")

        #extract identifiers
        processed_formula = process_sympy(formula)
        id = sympify(processed_formula)
        identifiers = id.atoms(Symbol)

        #create dictionary for formula identifiers
        formula_identifiers_json = Identifiers()

        #for each identifier
        for identifier in identifiers:

            identifier_symbol = str(identifier)

            print("Identifier Symbol: " + identifier_symbol)

            #identifier annotation recommendation
            identifier_feedback = "i"
            for formula_iter in formulae_json.Formulae:
                for identifier_iter in formula_iter.Identifiers:
                    if identifier_iter.Symbol == identifier_symbol:
                        identifier_feedback = input("Identifier Name: " + identifier_iter.Name + " yes/no/input?")
                        if identifier_feedback == "y" or identifier_feedback=="i":
                            break

            #ask for identifier name and QID
            if identifier_feedback == "y":
                identifier_name = identifier_iter.Name
                identifier_qid = identifier_iter.WikiQID
            else:
                identifier_name = input("Identifier Name: ")
                identifier_qid = input("Identifier QID: ")

            #store formula identifiers in json
            formula_identifiers_json.Identifiers.append(Identifier(identifier_symbol, identifier_name, identifier_qid))

        #store formulae with identifiers in json
        formulae_json.Formulae.append(Formula(formula, formula_name, formula_qid, formula_identifiers_json.Identifiers))

    return formulae_json