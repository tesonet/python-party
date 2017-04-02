import fileinput
import sys
import os

from soundex import count_soundex, is_alpha


def input_validation(cli_input):
    """ Input validation function """
    if len(cli_input) != 3:
        print('There must be exactly 2 parameters provided: 1) input file 2) search word')
        return False
    try:
        if not os.stat(sys.path[0] + '/' + cli_input[1]).st_size:
            print('The file is empty')
            return False
        else:
            if is_alpha(cli_input[2][0]):
                return True
            else:
                print('Please provide a string at least starting with an American letter')
                return False
    except FileNotFoundError:
        print('File does not exist in script directory. Please check again.')
        return False


def split_word(input_word):
    """ Stripping unnecessary common chars from word """
    input_word = input_word.rstrip('\n')
    input_word = input_word.strip(',')
    input_word = input_word.strip('()')
    input_word = input_word.strip('[]')
    input_word = input_word.strip('.')
    input_word = input_word.strip(':')
    input_word = input_word.strip('!')
    input_word = input_word.strip('?')
    return input_word


def compute_and_store(text_word):
    text_word = split_word(text_word)
    word_soundex = count_soundex(text_word)
    if word_soundex and word_soundex[0] == search_word_code[0]:
        if not similar_soundex.get(word_soundex):
            similar_soundex[word_soundex] = [text_word]
        else:
            similar_soundex[word_soundex].append(text_word)


if input_validation(sys.argv):
    """ Preparing given word for search """
    search_word_code = count_soundex(sys.argv[2])
    search_word_number = int(search_word_code[1:])

    similar_soundex = {}

    """ Reading file line by line, meanwhile putting only a single line in RAM """
    with fileinput.FileInput(sys.path[0] + '/' + sys.argv[1]) as file:
        for line in file:
            for word in line.split(' '):
                if '/' in word:
                    for i in word.split('/'):
                        compute_and_store(i)
                compute_and_store(word)

    """ Putting all the similar soundex codes into a seperate list for search of the best match """
    similar_soundex_keys = [d for d in similar_soundex.keys()]
    similar_soundex_keys = sorted(similar_soundex_keys)
    for index, i in enumerate(similar_soundex_keys):
        similar_soundex_keys[index] = int(i[1:])

    """ Finding the middle index of whole list and counting the difference from searching word
    code. It is done because searching from the start could take a lot of resources, especially,
    if best matching soundex code appears to be in the very end.
    """
    middle_index = int(len(similar_soundex_keys) / 2)
    difference_from_search = abs(similar_soundex_keys[middle_index] - search_word_number)
    matched_index = 0

    """ Starting from the middle to the higher soundex code or lower to find the best matching
    soundex code of searching word
    """
    if similar_soundex_keys[middle_index] < search_word_number:
        for i in range(middle_index, len(similar_soundex_keys)):
            if abs(similar_soundex_keys[i] - search_word_number) < difference_from_search:
                matched_index = i
                difference_from_search = abs(similar_soundex_keys[i] - search_word_number)
            else:
                break
    else:
        for i in reversed(range(0, middle_index)):
            if abs(similar_soundex_keys[i] - search_word_number) < difference_from_search:
                matched_index = i
                difference_from_search = abs(similar_soundex_keys[i] - search_word_number)
            else:
                break

    """ Putting best matched words to list, using best matched soundex code """
    matched_words_list = similar_soundex.get(
        search_word_code[0] + str(similar_soundex_keys[matched_index]))

    """ If the list of best matched soundex code does not contain 5 unique strings, 4 higher and
    4 lower elements from soundex codes list are taken (if available). These elements are put to
    the list and sorted, according to the difference from searching word code
    """
    other_values = list()
    if len(set(matched_words_list)) < 5:
        for number in range(1, 5):
            """ Trying to get higher elements from mostly matched one """
            try:
                higher_element = similar_soundex_keys[matched_index + number]
                other_values.append([higher_element, abs(higher_element - search_word_number)])
            except IndexError:
                pass
            """ Trying to get lower elements from mostly matched one """
            try:
                lower_element = similar_soundex_keys[matched_index - number]
                other_values.append([lower_element, abs(lower_element - search_word_number)])
            except IndexError:
                pass
        other_values = sorted(other_values, key=lambda x: x[1])
        for i in other_values:
            matched_words_list += similar_soundex.get(search_word_code[0] + str(i[0]))
            if len(set(matched_words_list)) >= 5:
                break

    """ Putting values to the list, until 5 unique strings are there. """
    printing_list = list()
    for i in matched_words_list:
        if not i in printing_list:
            printing_list.append(i)
        if len(printing_list) == 5:
            break
    if not len(printing_list):
        print('No similar word was found.')
    elif len(printing_list) != 5:
        print('Only {0} similar words were found:'.format(len(printing_list)))
    print('\n'.join(printing_list))
