"""Unit tests for find.py"""
import unittest
import multiprocessing
from click.testing import CliRunner
from find import read_in_chunks, get_words, find_words, score, soundex, get_results, main


class TestReadFile(unittest.TestCase):
    """Tests based on reading from file"""

    def compare_outcome(self, cases: tuple, msg=''):
        """Comapre method for test_read_chunks"""
        for file_path, chunk_size in cases:

            with open(file_path, 'r',encoding='utf8') as file_obj:
                contents = file_obj.read()

            with open(file_path, 'r',encoding='utf8') as file_obj:
                contents_to_test = ''
                for chunk in read_in_chunks(file_obj, chunk_size):
                    contents_to_test = ''.join([contents_to_test, chunk])

            self.assertEqual(contents_to_test, contents, msg)

    def test_read_chunks(self):
        """Check if iterating over generator gives same result as reading whole file into memory"""
        cases = (
            ('tests/test_data/test.txt', 2048),
            ('tests/test_data/test.txt', 50000),
            ('tests/test_data/plague_of_pythons.txt', 2048),
            ('tests/test_data/plague_of_pythons.txt', 50000),
            )
        msg = "Different read from file"
        self.compare_outcome(cases, msg)

    def test_read_chunks_long_string(self):
        """Iterating over file without spaces/newlines should raise RunTimeError"""
        with self.assertRaises(RuntimeError):
            find_words('tests/test_data/longstring.txt', 2048)
            find_words('tests/test_data/longstring.txt', 1024)
            find_words('tests/test_data/longstring.txt', 5000)

    def test_no_words(self):
        """Value error should be raised if no words found in file"""
        with self.assertRaises(ValueError):
            find_words('tests/test_data/nowords.txt', 2048)
            find_words('tests/test_data/nowords.txt', 1)

    def test_multi_vs_single(self):
        """Test if same set of words is obtained via single and multi-process fetching"""
        cases = (
            ('tests/test_data/test.txt', 2048),
            ('tests/test_data/test.txt', 50000),
            ('tests/test_data/plague_of_pythons.txt', 2048),
            ('tests/test_data/plague_of_pythons.txt', 50000)
            )
        msg = "Different words obtained"
        for file_path, chunk_size in cases:
            pool = multiprocessing.Pool(4)
            self.assertEqual(find_words(file_path, chunk_size), find_words(file_path, chunk_size, None, pool), msg)

    def test_get_words(self):
        """Test get_word method,it should only return unique words form string"""
        cases = (
            ('I_LOVE_PYTHON', {'I', 'LOVE', 'PYTHON'}),
            ('I_LOVE_PYTHON_PYTHON_PYTHON', {'I', 'LOVE', 'PYTHON'}),
            ('Ayyayaya coco jambo ayyayai Ayyayaya coco', {'Ayyayaya', 'coco', 'jambo', 'ayyayai'}),
            ('5543 &%^&* something here 34324**$$', {'something', 'here'}),
            ('W0ULD B3 GR3AT T0 H4V3 J0B', {'W', 'ULD', 'B', 'GR', 'AT', 'T', 'H', 'V', 'J', 'B'}),
            )
        for case_string, expected in cases:
            self.assertEqual(get_words(case_string), expected, "Words don't match")

class TestScoringAndRanking(unittest.TestCase):
    """Tests based on scoring and ranking"""
    def test_soundex(self):
        """Test for soundex method"""
        cases = (
            ('Python', 'P350'),
            ('Soundex', 'S532'),
            ('John', 'J500'),
            ('Josh', 'J200'),
            ('Joshua', 'J200')
            )
        msg = "Wrong Soundex Index"
        for word, index in cases:
            self.assertEqual(soundex(word)[1], index, msg)

    def test_score_type(self):
        """Test score method for type and format"""

        with self.assertRaises(TypeError):
            score(3232, 3232)
            score(False, None)
            score([], [])

        with self.assertRaises(ValueError):
            score('A3333', 'B33232')
            score('', '')
            score('AAAA', 'BBBB')
            score('1234', '4343')

    def test_score(self):
        """Test score method for results"""
        cases = (
            ('A100', 'A100', 5),
            ('A101', 'A100', 4),
            ('A111', 'A100', 3),
            ('A211', 'A100', 2),
            ('B111', 'A100', 1),
            ('R211', 'A100', 0),
            )
        msg = 'Wrong score given'

        for keyword, candidate, expected in cases:
            self.assertEqual(score(keyword, candidate), expected, msg)

    def test_get_results(self):
        """Test get_result method"""
        words = {'JOSH', 'JOHN', 'JOB', 'JOHHNY', 'JOJO', 'ZEBRA', 'TARGET', 'PLOT'}
        keyword = ('Joshua', 'J200')
        expected = {'JOSH', 'JOHN', 'JOB', 'JOHHNY', 'JOJO'}
        to_test = set()
        for word, _ in get_results(words, keyword[1]):
            to_test.add(word)
        self.assertEqual(to_test, expected, "Words don't match")

class TestClick(unittest.TestCase):
    """Test entire CLI
    NOTE:Must update if any of click arguments change"""

    def test_results(self):
        """Test results"""
        runner = CliRunner()
        cases = (
            (['tests/test_data/test.txt', 'lituania'], 'LITHUANIA:5'),
            (['tests/test_data/test.txt', 'latvia'], 'LATVIA:5'),
            (['tests/test_data/test.txt', 'lituania', '-w', '4'], 'LITHUANIA:5'),
            (['tests/test_data/test.txt', 'kalin', '-cs', '4'], 'KALININGRAD:4'),
            )
        for command, expected in cases:
            result = runner.invoke(main, command)
            self.assertIn(expected, result.output, "Wrong result")
            self.assertEqual(result.exit_code, 0, "Script didn't finish")

    def test_chunk_size(self):
        """Test chunk size"""
        runner = CliRunner()
        cases = (
            (['tests/test_data/test.txt', 'lituania', '-cs', '128'], 128),
            (['tests/test_data/test.txt', 'kalin'], 2), #default
            )
        for command, expected in cases:
            result = runner.invoke(main, command)
            self.assertIn(f'chunk size of {expected} kB', result.output, "Wrong chunk size")
            self.assertEqual(result.exit_code, 0, "Script didn't finish")

    def test_workers(self):
        """Test chunk size"""
        runner = CliRunner()
        cases = (
            (['tests/test_data/test.txt', 'lituania', '-w', '4'], 4),
            (['tests/test_data/test.txt', 'kalin'], 1),#default
            (['tests/test_data/test.txt', 'kalin', '-w', '8'], 8)
            )
        for command, expected in cases:
            result = runner.invoke(main, command)
            self.assertIn(f'Running with {expected} worker(s)', result.output, "Wrong workers")
            self.assertEqual(result.exit_code, 0, "Script didn't finish")

    def test_input(self):
        """Test user input"""
        runner = CliRunner()
        cases = (
            ['tests/test_data/test.txt', '4', '-w', 'lituania'],
            ['tests/test_data/missing.txt', 'missing'],
            ['tests/test_data/test.txt', 'lituania', '--optionX'],
            ['tests/test_data/test.txt', 'lituania', '-cs', '-w'],
            )
        for command in cases:
            result = runner.invoke(main, command)
            self.assertIsNotNone(result.exception)
