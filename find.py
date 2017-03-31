import fileinput
import sys
import os

from soundex import count_soundex


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
            if cli_input[2][0].isalpha():
                return True
            else:
                print('Please provide a string at least starting with a letter')
                return False
    except FileNotFoundError:
        print('File does not exist in script directory. Please check again.')
        return False

if input_validation(sys.argv):
    search_word_code = count_soundex(sys.argv[2])
    search_word_number = int(search_word_code[1:])
    similar_soundex = {}

    with fileinput.FileInput(sys.path[0] + '/' + sys.argv[1]) as file:
        for line in file:
            for word in line.split(' '):
                if '/' in word:
                    word = word.split('/')[0]
                word = word.rstrip('\n')
                word = word.strip(',')
                word = word.strip('()')
                word = word.strip('[]')
                word = word.strip('.')
                word_soundex = count_soundex(word)
                if word_soundex and word_soundex[0] == search_word_code[0]:
                    if not similar_soundex.get(word_soundex):
                        similar_soundex[word_soundex] = [word]
                    else:
                        similar_soundex[word_soundex].append(word)

    similar_soundex_keys = [d for d in similar_soundex.keys()]
    similar_soundex_keys = sorted(similar_soundex_keys)
    for index, i in enumerate(similar_soundex_keys):
        similar_soundex_keys[index] = int(i[1:])
    middle_index = int(len(similar_soundex_keys)/2)
    difference_from_search = abs(similar_soundex_keys[middle_index] - search_word_number)
    matched_index = 0
    if similar_soundex_keys[middle_index] < search_word_number:
        for l in range(middle_index, len(similar_soundex_keys)):
            if abs(similar_soundex_keys[l] - search_word_number) < difference_from_search:
                matched_index = l
                difference_from_search = abs(similar_soundex_keys[l] - search_word_number)
            else:
                break
    else:
        for l in reversed(range(0, middle_index)):
            if abs(similar_soundex_keys[l] - search_word_number) < difference_from_search:
                matched_index = l
                difference_from_search = abs(similar_soundex_keys[l] - search_word_number)
            else:
                break

    return_list = similar_soundex.get(search_word_code[0] + str(similar_soundex_keys[matched_index]))

    other_values = list()
    if len(set(return_list)) < 5:
        for number in range(1, 5):
            try:
                higher_element = similar_soundex_keys[matched_index+number]
                other_values.append([higher_element, abs(higher_element - search_word_number)])
            except IndexError:
                pass
            try:
                lower_element = similar_soundex_keys[matched_index-number]
                other_values.append([lower_element, abs(lower_element - search_word_number)])
            except IndexError:
                pass
        other_values = sorted(other_values, key=lambda x: x[1])
        for i in other_values:
            return_list += similar_soundex.get(search_word_code[0] + str(i[0]))
            if len(set(return_list)) >= 5:
                break
    new_l = list()
    for i in return_list:
        if not i in new_l:
            new_l.append(i)
        if len(new_l) == 5:
            break
