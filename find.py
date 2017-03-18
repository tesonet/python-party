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
    def drop_letters(string: str, letters: str) -> str:
        """Drop given letters from string."""
        dropped = string.translate(
            {ord(c): None for c in letters}
        )
        return dropped

    def drop_aeiouyhw(self, string: str) -> str:
        """Drop letters that are not required for the Soundex algorithm."""
        dropped = self.drop_letters(string, 'aeiou' + 'aeiou'.upper())
        dropped = self.drop_letters(dropped, 'yhw' + 'yhw'.upper())
        return dropped
