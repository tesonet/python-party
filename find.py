# -*- encoding: utf-8 -*-


class Soundex(object):
    """Class for keeping info on one word."""

    def __init__(self, string):
        self.string = string

    @property
    def rating(self):
        """Rating of the word"""
        return len(self.string)
