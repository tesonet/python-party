# -*- encoding: utf-8 -*-

import unittest2

from find import Soundex


class TestAll(unittest2.TestCase):
    """Starter Test Suite."""

    def setUp(self):
        """Setup common data."""
        super().setUp()

    def test_rating(self):
        """"""
        s = Soundex('123')
        self.assertEqual(s.rating, 3)