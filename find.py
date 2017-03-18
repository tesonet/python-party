# -*- encoding: utf-8 -*-

import re


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


def drop_letters(string: str, letters: str) -> str:
    """Drop given letters from string."""
    dropped = string.translate(
        {ord(c): None for c in letters}
    )
    return dropped


def assign_digits(string: str) -> str:
    """Assign rates to consonants according to Soundex."""
    # TODO Prettify map? Put somewhere reusable without rerun.
    _map = {
        ord('b'): ord('1'),
        ord('f'): ord('1'),
        ord('p'): ord('1'),
        ord('v'): ord('1'),
        ord('c'): ord('2'),
        ord('g'): ord('2'),
        ord('j'): ord('2'),
        ord('k'): ord('2'),
        ord('q'): ord('2'),
        ord('s'): ord('2'),
        ord('x'): ord('2'),
        ord('z'): ord('2'),
        ord('d'): ord('3'),
        ord('t'): ord('3'),
        ord('l'): ord('4'),
        ord('m'): ord('5'),
        ord('n'): ord('5'),
        ord('r'): ord('6'),
        ord('b'.upper()): ord('1'),
        ord('f'.upper()): ord('1'),
        ord('p'.upper()): ord('1'),
        ord('v'.upper()): ord('1'),
        ord('c'.upper()): ord('2'),
        ord('g'.upper()): ord('2'),
        ord('j'.upper()): ord('2'),
        ord('k'.upper()): ord('2'),
        ord('q'.upper()): ord('2'),
        ord('s'.upper()): ord('2'),
        ord('x'.upper()): ord('2'),
        ord('z'.upper()): ord('2'),
        ord('d'.upper()): ord('3'),
        ord('t'.upper()): ord('3'),
        ord('l'.upper()): ord('4'),
        ord('m'.upper()): ord('5'),
        ord('n'.upper()): ord('5'),
        ord('r'.upper()): ord('6'),
    }
    return string.translate(_map)


def merge_duplicates(string: str) -> str:
    """Merge duplicate chars in string."""
    # TODO Test.
    last = ''
    res = ''
    for c in string:
        if not c == last:
            res += c
        last = c
    return res


def rating(string: str) -> str:
    """
    Return American Soundex rating for the given string.
    
    Algorithm according to [https://en.wikipedia.org/wiki/Soundex](Wikipedia).
    
    1. Save the first letter. Remove all occurrences of 'h' and 'w' except first letter.
    2. Replace all consonants (include the first letter) with digits as in [2.] above.
    3. Replace all adjacent same digits with one digit.
    4. Remove all occurrences of a, e, i, o, u, y except first letter.
    5. If first symbol is a digit replace it with letter saved on step 1.
    6. Append 3 zeros if result contains less than 3 digits. Remove all except 
        first letter and 3 digits after it (This step same as [4.] in explanation above).
    
    Args:
        string (str): string to rate. 

    Returns:
        str: Soundex rating.
        
    Raises:
        TypeError: when not a string is passed.
        ValueError: when an empty string is passed.
    """
    if not type(string) == str:
        raise TypeError
    if not string:
        raise ValueError("Need at least one char in the string.")
    if re.search(r'[^a-zA-Z]+', string) is not None:
        raise ValueError("Only ASCII letters expected.")
    first_letter = string[0]
    step_one = drop_letters(string[1:], 'hw')
    step_two = assign_digits(first_letter + step_one)
    step_three = merge_duplicates(step_two)
    step_four = step_three[0] + drop_letters(step_three[1:], 'aeiouy')
    step_five = step_four
    if step_three[0].isdigit():
        step_five[0] = first_letter
    step_six = ''
    for num in range(4):
        try:
            step_six += step_five[num]
        except IndexError:
            step_six += '0'
    return step_six
