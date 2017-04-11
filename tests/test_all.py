# -*- encoding: utf-8 -*-

import unittest2

from find import soundex, sanitize_string, diff_score, Ranker


class TestSoundex(unittest2.TestCase):
    """Test Soundex rating method."""

    def test_soundex(self):
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
            ("Robert", "r163"),
            ("rubin", "r150"),
            ("Ashcraft", "a261"),
            ("ashcroft", "a261"),
            ("Tymczak", "t522"),
            ("Pfister", "p236"),

            # Additional tests for too short strings.
            ("Aciu", "a200"),
            ("tsun", "t250"),
            ("A", "a000"),
        )
        for string, res in expected:
            self.assertEqual(soundex(string), res)

    def test_soundex_ignores_case(self):
        """Should rank as if lowercase was submitted."""
        expected = (
            ("Rubin", "r150"),
            ("rubin", "r150"),
            ("rUbiN", "r150"),
        )
        for string, res in expected:
            self.assertEqual(soundex(string), res)

    def test_soundex_raises_on_empty(self):
        """Should raise when empty string is passed."""
        with self.assertRaises(ValueError):
            soundex('')

    def test_soundex_raises_on_not_string(self):
        """Should raise when empty string is passed."""
        with self.assertRaises(TypeError):
            soundex(1)
        with self.assertRaises(TypeError):
            soundex(TypeError)
        with self.assertRaises(TypeError):
            soundex(Soundex(''))
        with self.assertRaises(TypeError):
            soundex(False)
        with self.assertRaises(TypeError):
            soundex(True)
        with self.assertRaises(TypeError):
            soundex(None)
        with self.assertRaises(TypeError):
            soundex({})
        with self.assertRaises(TypeError):
            soundex([])
        with self.assertRaises(TypeError):
            soundex(tuple())
        with self.assertRaises(TypeError):
            soundex(set())

    def test_soundex_raises_on_string_not_only_letters(self):
        """Should raise when empty string is passed."""
        with self.assertRaises(ValueError):
            soundex("1")
        with self.assertRaises(ValueError):
            soundex("Ali3a3a")
        with self.assertRaises(ValueError):
            soundex("Užantis")


class TestMain(unittest2.TestCase):
    """Tests for main routine."""

    def test_sanitize_string(self):
        """Should return list of words, ascii only."""
        cases = (
            ("abc cde efg", ["abc", "cde", "efg"]),
            ("In the glorious Rome", ["In", "the", "glorious", "Rome"]),
            ("1'm n07 5ur3 ab0u7 7h15", ["m", "n", "ur", "ab", "u", "h"]),
            ("Some\nmulti-line", ["Some", "multi", "line"]),
            ("Listeni/ˌlɪθuːˈeɪniə/,[11][12][13]", ["Listeni", "l", "u", "e", "ni"]),
        )
        for start, expected in cases:
            self.assertEqual(sanitize_string(start), expected)


class TestDiffRanking(unittest2.TestCase):
    """Tests for calculation of difference between ranked words."""

    def _test_diff_score(self, cases: tuple, msg=''):
        """Helper for testing cases of `diff_score` tests."""
        for str1, str2, exp in cases:
            self.assertEqual(diff_score(str1, str2), exp, msg)

    def test_diff_score_same(self):
        """Should return 0 for diff score, when same ratings found."""
        cases = (
            ('T123', 'T123', 0),
            ('X000', 'X000', 0),
            ('A290', 'A290', 0),
        )
        msg = "0 should have been returned for the same ratings."
        self._test_diff_score(cases, msg)

    def test_diff_score_no_common(self):
        """Should return 2000 if strings are completely different."""
        cases = (
            ('T123', 'A987', 2000),
            ('E482', 'X000', 2000),
            ('P576', 'C333', 2000),
        )
        msg = "2000 whould have been returned for completely different ratings."
        self._test_diff_score(cases, msg)

    def test_diff_score_numbers_diff(self):
        """Should return difference in ratings, when only numbers differ."""
        cases = (
            ('T123', 'T156', 33),
            ('E482', 'E180', 302),
            ('P576', 'P577', 1),
        )
        msg = ("Difference in numerical values should have been returned for "
               "strings with the same first letter.")
        self._test_diff_score(cases, msg)

    def test_diff_score_letter_diff(self):
        """Should return +1000 score if letters differ."""
        cases = (
            ('T123', 'U156', 1033),
            ('A482', 'Z180', 1302),
            ('A576', 'B577', 1001),
        )
        msg = ("Score was not increased by 1000 for ratings of different "
               "first letter.")
        self._test_diff_score(cases, msg)


class TestRanker(unittest2.TestCase):
    """Tests for the Ranker class."""

    def test_init_default_result_2000(self):
        """Clean init should init `results` with score 2000 and a text."""
        r = Ranker()
        self.assertEqual(len(r.results), 1,
                         "Incorrect number of entries in `results`.")
        self.assertEqual(r.results, {2000: "No words found."},
                         "Wrong default `results`.")

    def test_init_default_limit_5(self):
        """Clean init should default `limit` to 5."""
        r = Ranker()
        self.assertEqual(r.limit, 5, "Wrong default `limit`.")

    def test_init_param_limit(self):
        """Should init `limit` to what is set when initializing."""
        cases = (1, 10, 3645, 10**5)
        for case in cases:
            r = Ranker(limit=case)
            self.assertEqual(r.limit, case, "Wrong init `limit`.")

    def test_init_param_limit_prevent_negative(self):
        """Should not allow negative `limit` values."""
        cases = (-1, -50, -1205530)
        for case in cases:
            with self.assertRaises(ValueError):
                Ranker(limit=case)

    def test_init_param_limit_prevent_zero(self):
        """Should not allow zero `limit` value."""
        with self.assertRaises(ValueError):
            Ranker(limit=0)

    def test_init_param_limit_only_int(self):
        """Should allow only int type for `limit`.."""
        cases = ('', True, {1: 2}, (1,), [1], 1.5, {1})
        for case in cases:
            with self.assertRaises(TypeError):
                Ranker(limit=case)

    def test_add_word_under_limit(self):
        """Should add a new word to results, when there is space."""
        msg = "Word not added."
        r = Ranker()
        r.add_word(123, "Rating")
        self.assertEqual(
            r.results,
            {2000: "No words found.", 123: "Rating"},
            msg,
        )
        r.add_word(22, "Another")
        self.assertEqual(
            r.results,
            {2000: "No words found.", 123: "Rating", 22: "Another"},
            msg,
        )

    def test_add_word_just_at_limit(self):
        """Should add a new word to results, when there one space left."""
        r = Ranker(limit=2)
        r.add_word(123, "Rating")
        self.assertEqual(
            r.results,
            {2000: "No words found.", 123: "Rating"},
            "Word not added.",
        )

    def test_add_word_replace_word_above_limit(self):
        """Should replace unworthy word, if there is limit."""
        r = Ranker(limit=1)
        r.add_word(123, "Rating")
        self.assertEqual(
            r.results,
            {123: "Rating"},
            "Default scored word not replaced above limit (1).",
        )

    def test_add_word_replace_highest_score_above_limit(self):
        """Should replace the highest score above added word's score, limit."""
        r = Ranker(limit=3)
        r.add_word(123, "Rating")
        r.add_word(456, "Another")
        r.add_word(200, "TwoH")
        self.assertEqual(
            r.results,
            {
                123: "Rating",
                200: "TwoH",
                456: "Another",
            },
            "Highest score not replaced by lower one."
        )

    def test_add_word_not_replace_if_unworthy_above_limit(self):
        """Should not replace any if the given score is above max results."""
        r = Ranker(limit=2)
        r.add_word(123, "Rating")
        r.add_word(9000, "Over 9000")
        self.assertEqual(
            r.results,
            {
                123: "Rating",
                2000: "No words found.",
            },
            "A higher should not have replaced a lower one."
        )

    def test_add_word_no_add_duplicate_scores(self):
        """Should not add a duplicate score."""
        r = Ranker()
        r.add_word(2000, "Duplicate")
        self.assertEqual(
            r.results,
            {2000: "No words found."},
            "Should not have added a duplicate score."
        )

    def test_add_word_no_replace_duplicate_scores(self):
        """Should not replace a word with a duplicate score."""
        r = Ranker(limit=2)
        r.add_word(123, "Ranking")
        r.add_word(123, "Not a ranking.")
        self.assertEqual(
            r.results,
            {2000: "No words found.", 123: "Ranking"},
            "Should not have replaced with a duplicate score."
        )

    def test_get_results_returns_list(self):
        """Should return list."""
        r = Ranker()
        res = r.get_results()
        self.assertEqual(type(res), list, "Wrong type returned.")

    def test_get_results_returns_sorted_results(self):
        """Should return results sorted by score."""
        r = Ranker()
        r.add_word(123, "Ranking")
        r.add_word(456, "Another")
        r.add_word(0, "Absolute zero")
        res = r.get_results()
        self.assertEqual(
            res,
            [
                (0, "Absolute zero"),
                (123, "Ranking"),
                (456, "Another"),
            ],
            "The results should have been sorted."
        )

    def test_get_results_clean_default_score(self):
        """Should not have a default 2000 score in get_results, if others exist."""
        r = Ranker()
        r.add_word(123, "Rating")
        res = r.get_results()
        self.assertNotIn(
            (2000, "No words found."),
            res,
            "Default value should have been removed."
        )

    def test_get_results_default_score_if_only(self):
        """Should return default results, if no other scores are inside."""
        r = Ranker()
        res = r.get_results()
        self.assertEqual(
            res,
            [(2000, "No words found.")],
            "Default score should have been retained when there are no others."
        )