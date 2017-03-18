# -*- encoding: utf-8 -*-


class Soundex(object):
    """Class for keeping info on one word."""

    def __init__(self, string=''):
        self.string = string

    @property
    def rating(self):
        """Rating of the word"""
        return len(self.string)

    @staticmethod
    def drop_aeiouyhw(string: str) -> str:
        """Drop letters that are not required for the Soundex algorithm."""
        letters = 'aeiouyhw'
        dropped = string.translate(
            {ord(c): None for c in letters + letters.upper()}
        )
        return dropped
