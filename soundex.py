def count_soundex(word):
    """ Soundex algorithm """
    word = word.upper()
    first_letter_index = 0
    for i in word:
        if i.isalpha():
            first_letter_index = word.index(i)
            break
    coded_word = ""
    coded_word += word[first_letter_index]

    CONSTANTS = {
        "AEIOUY": ".",
        "HW": "#",
        "BFPV": "1",
        "CGJKQSXZ": "2",
        "DT": "3",
        "L": "4",
        "MN": "5",
        "R": "6",
    }
    for key in CONSTANTS.keys():
        if word[first_letter_index] in key:
            first_char_code = CONSTANTS[key]

    for char in word[first_letter_index+1:]:
        for key in CONSTANTS.keys():
            if char in key:
                code = CONSTANTS[key]
                if coded_word[-1] == word[0] and first_char_code:
                    if code != first_char_code:
                        coded_word += code
                elif coded_word[-1] == '#':
                    if code != coded_word[-2]:
                        coded_word += code
                else:
                    first_char_code = None
                    if code != coded_word[-1]:
                        coded_word += code

    coded_word = coded_word.replace(".", "")
    coded_word = coded_word.replace("#", '')
    coded_word = coded_word[:4].ljust(4, "0")
    return coded_word
