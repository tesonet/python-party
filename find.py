# -*- encoding: utf-8 -*-
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait, as_completed
import timeit
from functools import lru_cache, partial
import operator
import re

import click


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


@lru_cache(maxsize=None)
def soundex(string: str) -> str:
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
    string = string.lower()
    first_letter = string[0]
    step_one = drop_letters(string[1:], 'hw')
    step_two = assign_digits(first_letter + step_one)
    step_three = merge_duplicates(step_two)
    step_four = step_three[0] + drop_letters(step_three[1:], 'aeiouy')
    step_five = step_four
    if step_three[0].isdigit():
        step_five = first_letter + step_five[1:]
    step_six = ''
    for num in range(4):
        try:
            step_six += step_five[num]
        except IndexError:
            step_six += '0'
    return step_six


def sanitize_string(word: str) -> list:
    """Returned list of sanitized words from the string."""
    return re.compile(r'[a-zA-Z]+').findall(word)


def diff_score(base: str, opp: str) -> int:
    """Give difference score between `base` and `opp` strings."""
    score = 0
    # Same.
    if base == opp:
        return 0
    # Completely different.
    elif not set(base) & set(opp):
        return 2000
    # First letter coincides.
    if base[0] != opp[0]:
        score += 1000
    # The numerical value of rating.
    score += abs(int(base[1:]) - int(opp[1:]))
    return score


class Ranker(object):
    """Class for holding the list of highest ranking words."""

    def __init__(self, limit=5):
        # Checks.
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise TypeError("Only integers allowed for `limit`.")
        elif limit <= 0:
            raise ValueError("Only positive values allowed for `limit`.")
        # Assignments.
        self.results = {
            2000: "No words found."
        }
        self.limit = limit

    def add_word(self, score: int, word: str):
        """Add word to results, if worthy."""
        if score not in self.results:
            max_diff = max(self.results)
            if score < max_diff:
                if len(self.results) >= self.limit:
                    self.results.pop(max_diff)
                self.results[score] = word

    def merge_ranker(self, ranker):
        """Merge another Ranker to this one."""
        for score, word in ranker.results.items():
            self.add_word(score, word)

    def get_results(self) -> list:
        """Return results sorted by key."""
        # Do not consider the default value.
        if len(self.results) > 1 and 2000 in self.results:
            self.results.pop(2000)
        return sorted(self.results.items(), key=operator.itemgetter(0))


def gen_chunks(file, chunk_size=10000) -> list:
    """Read `file` and yield the lines up to the `chunk_size` at a time."""
    res = True
    while res:
        res = file.readlines(chunk_size)
        if res:
            yield res  # Read `chunk_size` chars worth of complete lines.


def analyze_chunk(chunk: list, base_rating: str) -> Ranker:
    """Analyze a list of lines against the `base_rating`."""
    rankings = Ranker()
    for line in chunk:
        # In case the line does not contain anything useful (for .decode).
        if not line:
            break
        words = line.decode('utf-8')
        sanitized_words = sanitize_string(words)
        for word in sanitized_words:
            word_rating = soundex(word)
            diff = diff_score(base_rating, word_rating)
            rankings.add_word(diff, word)
    return rankings


def do_concurrent(base_rating, file, chunk_size=10000, max_workers=7):
    """Analyze the file concurrently."""
    # TODO Do not read the file until it is necessary for next analysis.
    # Currently, the full file is mapped to the functions, meaning oen needs
    # at least as much RAM as the size of file.
    ratings = Ranker()
    analyze = partial(analyze_chunk, base_rating=base_rating)
    # This can act as a single-thread as well.
    # for chunk_ratings in map(analyze, gen_chunks(file)):
    #     ratings.merge_ranker(chunk_ratings)

    # This is the multi-process part.
    executor = ProcessPoolExecutor(max_workers=max_workers)
    for chunk_ratings in executor.map(analyze, gen_chunks(file, chunk_size)):
        ratings.merge_ranker(chunk_ratings)
    executor.shutdown(wait=True)  # Wait for all executors to finish.

    return ratings


@click.command()
@click.argument('file', type=click.File('rb'))
@click.argument('string')
@click.option('--concurrent', '-c', is_flag=True)
@click.option('--workers', '-w', default=1)
@click.option('--chunk_size', '-cs', default=10000)
def main(file, string, concurrent, workers, chunk_size):
    """Main entry to script."""
    start = timeit.default_timer()
    base_rating = soundex(string)
    if not concurrent:
        print("Analyzing in one thread.")
        res = Ranker()
        base_rating = soundex(string)
        for line in file:
            words = line.decode('utf-8')
            sanitized_words = sanitize_string(words)
            for word in sanitized_words:
                word_rating = soundex(word)
                diff = diff_score(base_rating, word_rating)
                res.add_word(diff, word)
    else:
        print(f"Analyzing concurrently, using {workers} workers "
              f"and chunk_size of {chunk_size}.")
        if chunk_size < 4000:
            print("WARNING: You might experience lower performance due to "
                  "chunk_size being low (less than 4000).\n"
                  "It is recommended to give 1500 chunk_size for each worker "
                  "with a minimum of 4000.")
        res = do_concurrent(base_rating, file,
                            max_workers=workers, chunk_size=chunk_size)

    # TODO Clean up.
    from pprint import pprint
    pprint(res.get_results())
    end = timeit.default_timer()
    pprint(f"Script took {end - start} seconds.")

if __name__ == '__main__':
    main()
