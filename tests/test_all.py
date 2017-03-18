# -*- encoding: utf-8 -*-

import unittest2


class TestAll(unittest2.TestCase):
    """Starter Test Suite."""

    def setUp(self):
        """Setup common data."""
        super().setUp()

    def test_2_plus_2(self):
        """2 + 2 = 4?"""
        self.assertEqual(2+2, 4, "Sum incorrect.")
