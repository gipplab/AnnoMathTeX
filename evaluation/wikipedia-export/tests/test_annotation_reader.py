from mathqidupdater.annotation_reader import get_file_list
import unittest


class TestAnnotationReader(unittest.TestCase):
    def test_file_list(self):
        files = get_file_list('./data')
        self.assertEqual(files, ['Harmonic_oscillator.csv', 'Jerk_(physics).csv'])
