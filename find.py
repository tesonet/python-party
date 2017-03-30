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
    print(search_word_code)


