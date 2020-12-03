import logging
import sys
import unittest
from mathqidupdater.wikitext_replacer import WikitextReplacer


class TestWikitextReplacer(unittest.TestCase):
    sample = open('./data/Harmonic_oscillator.txt', 'r', encoding='utf-8').read()
    replacements = {' \\vec F = -k \\vec x, ': '170282',
                    ' x(t) = A \\cos(\\omega t + \\varphi), ': '3299367',
                    'F = m a = m \\frac{\\mathrm{d}^2x}{\\mathrm{d}t^2} = m\\ddot{x} = -k x. ': '170282',
                    '\\omega = \\sqrt{\\frac k m}.': '834020'}

    def test_get_math_tags(self):
        replacer = WikitextReplacer(self.sample, self.replacements)
        real = replacer.replace_math_tags()
        self.assertTrue(real.__contains__('math'))

    def test_get_bot(self):
        replacer = WikitextReplacer('{{bots}}', self.replacements)
        self.assertTrue(replacer.allow_bots('ZentralBot'))
        replacer = WikitextReplacer('{{nobots}}', self.replacements)
        self.assertFalse(replacer.allow_bots('ZentralBot'))
        replacer = WikitextReplacer('{{bots|allow=all}}', self.replacements)
        self.assertTrue(replacer.allow_bots('ZentralBot'))
        replacer = WikitextReplacer('{{bots|deny=all}}', self.replacements)
        self.assertFalse(replacer.allow_bots('ZentralBot'))
        replacer = WikitextReplacer('{{bots|deny=ZentralBot}}', self.replacements)
        self.assertFalse(replacer.allow_bots('ZentralBot'))
        replacer = WikitextReplacer('{{not-specified}}', self.replacements)
        self.assertTrue(replacer.allow_bots('any'))




logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

