#taken from https://github.com/ag-gipp/MathQa/blob/master/latexformlaidentifiers.py
#made some changes


import ast
import parser
import re
from sympy.parsing.latex import parse_latex
from sympy.utilities.mathml import c2p
from sympy.core.sympify import sympify
from sympy import Number, NumberSymbol, Symbol
from sympy.printing.latex import latex
from sympy.printing.mathml import mathml
from sympy import *
from collections import OrderedDict


import logging
logging.basicConfig(level=logging.DEBUG)
__LOGGER__ = logging.getLogger(__name__)

# import scipy.constants
contant = {'pi': '3.141592653589793', 'golden': '1.618033988749895', 'golden_ratio': '1.618033988749895',
           'c': '299792458.0', 'speed_of_light': '299792458.0', 'mu_0': '1.2566370614359173e-06', \
           'epsilon_0': '8.854187817620389e-12', 'Planck': '6.62607004e-34', 'hbar': '1.0545718001391127e-34',
           'G': '6.67408e-11', 'mu_{0}': '1.2566370614359173e-06', \
           'gravitational_constant': '6.67408e-11', 'g': '9.80665', 'e': '1.6021766208e-19',
           'elementary_charge': '1.6021766208e-19', 'gas_constant': '8.3144598', \
           'alpha': '0.0072973525664', 'fine_structure': '0.0072973525664', 'N_A': '6.022140857e+23',
           'Avogadro': '6.022140857e+23', 'k': '1.38064852e-23', \
           'Boltzmann': '1.38064852e-23', 'sigma': '5.670367e-08', 'Stefan_Boltzmann': '5.670367e-08',
           'Wien': '0.0028977729', 'Rydberg': '10973731.568508', \
           'm_e': '9.10938356e-31', 'electron_mass': '9.10938356e-31', 'm_p': '1.672621898e-27',
           'proton_mass': '1.672621898e-27', 'm_n': '1.672621898e-27', 'neutron_mass': '1.672621898e-27',
           'S': '5.24411510858423962092'}


def prepformula(formula):
    """
        Process of formula
    """

    replace = {"{\displaystyle": "", "\\tfrac": "\\frac", "\\left": "", "\\right": "", "\\mathrm": "", "\\textbf": "",
               "\\begin": "", "\end": "", "\\bigg": "", "\\vec": ""}

    if formula.startswith('{\displaystyle') and formula.endswith('}'):
        fformula = formula.rsplit('}', 1)
        return replace_all(fformula[0], replace)

    if formula.endswith('.'):
        fformula = formula.split('.')
        return replace_all(fformula[0], replace)

    if formula.endswith(","):
        fformula = formula.split(',')
        return replace_all(fformula[0], replace)

    else:
        return replace_all(formula, replace)


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def getlatexformula(formula):
    pformula = prepformula(formula)
    #print('In getlatexformula, pformula: {}'.format(pformula))
    f = parse_latex(pformula)
    #print('In getlatexformula, f: {}'.format(f))
    global latexformula
    latexformula = sympify(f)
    #print('formula: {} , latexformula: {} , pformula: {} , f: {}'.format(formula, latexformula, pformula, f))
    return latexformula


def evalformula(formula):
    #print('in Latexformula')
    latexformula = getlatexformula(formula)
    #print('latexformula: {}'.format(latexformula))
    l = sympify(latexformula)
    symbol = l.atoms(Symbol)
    #print('symbol: {} , l: {}'.format(symbol, l))
    return symbol, l
    #return symbol


"""def equality(formula, ext):
    global lhs
    global rhs
    lhs, rhs = formula.split(ext, 1)
    #print('lhs: {} , rhs: {}'.format(lhs, rhs))
    value = evalformula(rhs)
    
    return {'lhs': lhs}
    
    #return value"""


def formuladivision(formula):
    k = ['=', '\leq', '\req', '\\approx']
    if '=' in formula:
        ext = '='
        return ext

    if '\leq' in formula:
        ext = '\leq'
        return ext

    if '\req' in formula:
        ext = '\req'
        return ext

    if '\\approx' in formula:
        ext = '\\approx'
        return ext

    if not any(ext in formula for ext in k):
        return None



class ErrorHandler:

    def handle(self, error):
        message, formula, position = str(error).split('\n')
        position = len(position)
        if 'I expected one of these:' in message:
            expected_char = message[-2]
            new_formula = formula[:position] + ' {}'.format(expected_char) + formula[position:]
            __LOGGER__.info( 'ERROHANDLER, new formula: {}'.format(new_formula))

        if 'I don\'t understand this' in message:
            new_formula = formula[:position] + formula[position+1:]
            __LOGGER__.info('ERROHANDLER, new formula: {}'.format(new_formula))

        try:
            symbols, _ = evalformula(new_formula)
            symbols = {str(s) for s in symbols}
            return symbols
        except Exception as e:
            return self.handle(e)


class FormulaSplitter:

    #todo: remove special symbols
    def __init__(self, request):
        self.formula = self.remove_special_characters(request)
        global seprator
        seprator = formuladivision(self.formula)

    def remove_special_characters(self, request):
        #intab = ""
        #outtab = ""
        #trantab = maketrans(intab, outtab)
        #request_special_chars_removed =  request.translate(string.maketrans("", "", ), special_characters)
        special_characters = ['\{', '\}']
        request_special_chars_removed = request
        for special_char in special_characters:
            request_special_chars_removed = request_special_chars_removed.replace(special_char, '')
        return request_special_chars_removed


    def get_identifiers(self):
        try:
            symbols, _ = evalformula(self.formula)
            symbols = {str(s) for s in symbols}
            __LOGGER__.debug(' Symbols: {}'.format(symbols))
        except Exception as e:
            __LOGGER__.error(' Error in Formula Splitter: {}'.format(e))
            #__LOGGER__.info(' errormessage type: {}'.format(str(e)))
            #symbols = ErrorHandler().handle(e)
            symbols = None

        return symbols

    def get_formula(self):
        _, formula = evalformula(self.formula)
        formula_dict = {
                    'string': str(formula),
                    'latex': latex(formula),
                    'mathml': mathml(formula)
                }
        #print('MATHML: ', formula_dict['mathml'])
        return formula_dict

