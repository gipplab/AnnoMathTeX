from mathqidupdater.annotation_reader import get_file_list, get_qids
import unittest


class TestAnnotationReader(unittest.TestCase):
    def test_file_list(self):
        files = get_file_list('./data')
        self.assertEqual(files, ['Harmonic_oscillator.csv', 'Jerk_(physics).csv'])

    def test_get_qids(self):
        qids = get_qids('./data/Harmonic_oscillator.csv')
        self.assertEqual(qids, {' \\vec F = -k \\vec x, ': '170282',
                                ' x(t) = A \\cos(\\omega t + \\varphi), ': '3299367',
                                'F = m a = m \\frac{\\mathrm{d}^2x}{\\mathrm{d}t^2} = m\\ddot{x} = -k x. ': '170282',
                                '\\omega = \\sqrt{\\frac k m}.': '834020'})
