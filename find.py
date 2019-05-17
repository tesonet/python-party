"""Script for finding words similar to keyword using soundex index"""

import re
import unicodedata
import time
import multiprocessing
import os
from typing import Optional, List, Tuple, TextIO, Generator
from tqdm import tqdm #type: ignore
import click

def is_string(to_check: str) -> Optional[TypeError]:
    """raises TypeError if input is not a string"""
    if not isinstance(to_check, str):
        raise TypeError(f'expected str , got {type(to_check).__name__}')
    return None

def read_in_chunks(file_obj: TextIO, chunk_size: int = 2048, tqdm_bar: Optional[Tuple] = None) -> Generator:
    """Read file in chunkSize to the nearest newline or space; avoiding breaking individual words"""
    while True:
        data = file_obj.read(chunk_size)
        if not data:
            if tqdm_bar:
                tqdm_bar[1].n = tqdm_bar[0]
                tqdm_bar[1].set_description(desc="File loaded")
            break
        increment = 0
        while data[-1:] != '\n' and data[-1] != ' ':
            increment += 1
            add_more = file_obj.read(1)
            data += add_more
            if increment > 250:
                raise RuntimeError("Long string detected:there might be no words seperated by spaces or newlines; please check the file")
            if not add_more:
                break
        if tqdm_bar:
            tqdm_bar[1].update(chunk_size)
        yield data

def get_words(chunk: str) -> set:
    """Return set of words from chunk of file(str)"""
    is_string(chunk)
    return set(re.compile(r'[a-zA-Z]+').findall(chunk))

def find_words(filepath: str, chunk_size: int = 2048, tqdm_bar: Optional[Tuple] = None, pool=None) -> set:
    """Return set of unique words from whole file, can be run in multiple processes."""
    words = set() #type: set
    with open(filepath, 'r',encoding='utf8') as file_obj:
        read_file = read_in_chunks(file_obj, chunk_size, tqdm_bar)
        if not pool: #Single processs
            for chunk in read_file:
                words |= get_words(chunk)
        else:#Use process pool provided
            map_words = pool.imap_unordered(get_words, read_file)
            for result in map_words:
                words |= result

            pool.close()
            pool.join()
    if not words:
        raise ValueError("No words found in file")
    return words

def soundex(keyword: str) -> Tuple[str, str]:
    """ Standard soundex algorithm, returns tuple with keyword and index for given keyword """
    is_string(keyword)

    if not keyword:
        raise ValueError("String cannot be empty.")

    unicodedata.normalize('NFKD', keyword)

    keyword = keyword.upper()

    replacements = (('BFPV', '1'),
                    ('CGJKQSXZ', '2'),
                    ('DT', '3'),
                    ('L', '4'),
                    ('MN', '5'),
                    ('R', '6'))
    result = [keyword[0]]
    count = 1

    for lset, sub in replacements:
        if keyword[0] in lset:
            last = sub # type: Optional[str]
            break
    else:
        last = None

    for letter in keyword[1:]:
        for lset, sub in replacements:
            if letter in lset:
                if sub != last:
                    result.append(sub)
                    count += 1
                last = sub
                break
        else:
            last = None
        if count == 4:
            break

    result += '0'*(4-count)
    return (keyword, ''.join(result))

def score(keyword: str, candidate: str) -> int:
    """Compare given keyword against candidates using soundex index and return score 0-5, 5 score meaning perfect match"""
    is_string(keyword)
    is_string(candidate)

    if any((len(keyword) != 4, len(candidate) != 4)):
        raise ValueError("Soundex index must 4 characters long")
    for each in (keyword, candidate):
        if re.match(r"[a-zA-Z]{1}\d{3}", each) is None:
            raise ValueError("Soundex index in wrong format")

    rank = 0
    for num, letter in enumerate(keyword):
        if letter == candidate[num]:
            if num == 0:
                rank += 2
            else:
                rank += 1
    return rank

def get_results(words: set, keyword: str) -> List[Tuple[str, int]]:
    """Given set of unique words from file, return first 5 words that are most similar to keyword """
    answer = sorted([(x, score(keyword, n)) for x, n in tuple(map(soundex, words))], key=lambda li: li[1], reverse=True)
    return answer[0:5]

def progress_bar(filepath: str) -> Optional[tuple]:
    '''Generate progress bar if os filesize is available, else return None'''
    total_size = os.stat(filepath).st_size
    if total_size:
        pbar = tqdm(total=total_size)
        pbar.set_description(desc="Reading file")
        return (total_size, pbar)
    return None

@click.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.argument('keyword')
@click.option('--workers', '-w', type=click.INT, default=1)
@click.option('--chunk_size', '-cs', type=click.INT, default=0)

def main(filepath, keyword, workers, chunk_size):
    """Main method for pulling click arguments and setting up enviroment"""
    start = time.time()
    keyword = soundex(keyword)
    tqdm_bar = progress_bar(filepath)
    #Different default chunk size for single/multi process
    if not chunk_size:
        if not workers or workers == 1:
            chunk_size = 2
        else:
            chunk_size = 128

    #Set up pool if more than 1 workers selected
    if workers < 1:
        pool = None
    else:
        # multiprocessing.set_start_method('spawn',force=True)
        pool = multiprocessing.Pool(workers)

    #Display/print depending if progress bar was generated, print breaks tqdm visually.
    if tqdm_bar:
        tqdm.write(f'Running with {workers} worker(s) and chunk size of {chunk_size} kB')
    else:
        print(f'Running with {workers} worker(s) and chunk size of {chunk_size} kB')

    #Translate to bytes
    chunk_size *= 1024

    #Read file>get words->soundex->score->sort
    words = find_words(filepath, chunk_size, tqdm_bar, pool)
    results = get_results(words, keyword[1])

    end = time.time()-start

    #Display/print results.
    if tqdm_bar:
        tqdm_bar[1].set_description(desc="Matches found")
        tqdm.write(f'Matches for {keyword} are: (5= perfect match, 0=least perfect match')
        tqdm.write(''.join(list(str(x)+':'+str(n)+' \n' for x, n in results[0:5])))
        tqdm.write(f'Time elapsed: {end:.4f} sec.')
    else:
        print(''.join(list(str(x)+':'+str(n)+' \n' for x, n in results[0:5])))
        print(f'Time elapsed: {end:.4f} sec.')

if __name__ == '__main__':
    main()
