# -*- encoding: utf-8 -*-

import string
import unittest2

from find import Soundex


class TestDrop(unittest2.TestCase):
    """Tests for dropping letters."""

    def setUp(self):
        """Setup common data."""
        super().setUp()
        self.drop_aeiouyhw_cases = (
            (string.ascii_lowercase, "bcdfgjklmnpqrstvxz"),
            (string.ascii_lowercase.upper(), "bcdfgjklmnpqrstvxz".upper()),
            ("America", "mrc"),
            ("Emporium", "mprm"),
            ("Imperial", "mprl"),
            ("Occasional", "ccsnl"),
            ("Uppercase", "pprcs"),
            ("Yarn", "rn"),
            ("Humanitarian", "mntrn"),
            ("Worthwhile", "rtl"),
            ("In the galaxy far far away", "n t glx fr fr "),
        )
        self.drop_aeiouyhw_cases_single_letter = (
            case[0] for case in self.drop_aeiouyhw_cases)

    def test_drop_letters(self):
        """Should drop given letters."""
        for case in self.drop_aeiouyhw_cases_single_letter:
            for letter in string.ascii_letters:
                self._test_drop(Soundex.drop_letters, case, letter)

    def _test_drop(self, func, string: str, letters: str):
        """Helper to test that some letter was dropped from the string."""
        for letter in letters:
            result = func(string, letter)
            self.assertEqual(
                result.find(letter), -1, f"Letter '{letter}' was not dropped.")

    def test_drop_drops_a(self):
        """Should drop letter 'a' from string."""
        letters = 'aA'
        strings = self.drop_aeiouyhw_cases_single_letter
        for string in strings:
            self._test_drop(Soundex.drop_letters, string, letters)

    def test_drop_drops_e(self):
        """Should drop letter 'e' from string."""
        letters = 'eE'
        strings = self.drop_aeiouyhw_cases_single_letter
        for string in strings:
            self._test_drop(Soundex.drop_letters, string, letters)

    def test_drop_drops_i(self):
        """Should drop letter 'i' from string."""
        letters = 'iI'
        strings = self.drop_aeiouyhw_cases_single_letter
        for string in strings:
            self._test_drop(Soundex.drop_letters, string, letters)

    def test_drop_drops_o(self):
        """Should drop letter 'i' from string."""
        letters = 'oO'
        strings = self.drop_aeiouyhw_cases_single_letter
        for string in strings:
            self._test_drop(Soundex.drop_letters, string, letters)

    def test_drop_drops_u(self):
        """Should drop letter 'u' from string."""
        letters = 'uU'
        strings = self.drop_aeiouyhw_cases_single_letter
        for string in strings:
            self._test_drop(Soundex.drop_letters, string, letters)

    def test_drop_drops_y(self):
        """Should drop letter 'y' from string."""
        letters = 'yY'
        strings = self.drop_aeiouyhw_cases_single_letter
        for string in strings:
            self._test_drop(Soundex.drop_letters, string, letters)

    def test_drop_drops_h(self):
        """Should drop letter 'h' from string."""
        letters = 'hH'
        strings = self.drop_aeiouyhw_cases_single_letter
        for string in strings:
            self._test_drop(Soundex.drop_letters, string, letters)

    def test_drop_drops_w(self):
        """Should drop letter 'w' from string."""
        letters = 'wW'
        strings = self.drop_aeiouyhw_cases_single_letter
        for string in strings:
            self._test_drop(Soundex.drop_letters, string, letters)

    def test_drop_drops_all(self):
        """Should drop the 'aeiouyhw' from string."""
        for string, exp_result in self.drop_aeiouyhw_cases:
            result = Soundex().drop_aeiouyhw(string)
            self.assertEqual(result, exp_result, "Wrong drop result.")