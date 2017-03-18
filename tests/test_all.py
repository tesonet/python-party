# -*- encoding: utf-8 -*-

import string
import unittest2

from find import Soundex, rating


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


class TestRating(unittest2.TestCase):
    """Test Soundex rating method."""

    def test_rating(self):
        """
        Using this algorithm, both "Robert" and "Rupert" return the same
        string "R163" while "Rubin" yields "R150".

        "Ashcraft" and "Ashcroft" both yield "A261" and not "A226"
        (the chars 's' and 'c' in the name would receive a single number
        of 2 and not 22 since an 'h' lies in between them).

        "Tymczak" yields "T522" not "T520" (the chars 'z' and 'k' in the
        name are coded as 2 twice since a vowel lies in between them).

        "Pfister" yields "P236" not "P123" (the first two letters have
        the same number and are coded once as 'P').
        """
        expected = (
            # Tests from wikipedia.
            ("Robert", "R163"),
            ("Rubin", "R150"),
            ("Ashcraft", "A261"),
            ("Ashcroft", "A261"),
            ("Tymczak", "T522"),
            ("Pfister", "P236"),

            # Additional tests for too short strings.
            ("Aciu", "A200"),
            ("Tsun", "T250"),
            ("A", "A000"),
        )
        for string, res in expected:
            self.assertEqual(rating(string), res)

    def test_rating_raises_on_empty(self):
        """Should raise when empty string is passed."""
        with self.assertRaises(ValueError):
            rating('')

    def test_rating_raises_on_not_string(self):
        """Should raise when empty string is passed."""
        with self.assertRaises(TypeError):
            rating(1)
        with self.assertRaises(TypeError):
            rating(TypeError)
        with self.assertRaises(TypeError):
            rating(Soundex(''))
        with self.assertRaises(TypeError):
            rating(False)
        with self.assertRaises(TypeError):
            rating(True)
        with self.assertRaises(TypeError):
            rating(None)
        with self.assertRaises(TypeError):
            rating({})
        with self.assertRaises(TypeError):
            rating([])
        with self.assertRaises(TypeError):
            rating(tuple())
        with self.assertRaises(TypeError):
            rating(set())

    def test_rating_raises_on_string_not_only_letters(self):
        """Should raise when empty string is passed."""
        with self.assertRaises(ValueError):
            rating("1")
        with self.assertRaises(ValueError):
            rating("Ali3a3a")
        with self.assertRaises(ValueError):
            rating("Užantis")

