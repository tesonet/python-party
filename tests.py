import unittest
from soundex import count_soundex


class SoundexTests(unittest.TestCase):

    def setUp(self):
        """ Initiating the list of words and their soundex code lists for testing
        soundex funtion"""
        self.testList = [
            ["Robert", "R163"],
            ["Rupert", "R163"],
            ["Rubin", "R150"],
            ["Ashcraft", "A261"],
            ["Ashcroft", "A261"],
            ["Tymczak", "T522"],
            ["Pfister", "P236"],
            ["lituania", "L350"],
            ["Lithuania", "L350"],
            ["Lithuanian", "L355"],
            ["Lietuva", "L310"],
            ["Listeni", "L235"],
            ["living", "L152"],
            ["Ashcraft", "A261"],
            ["Ashcroft", "A261"],
            ["auerbach", "A612"],
            ["Baragwanath", "B625"],
            ["bar", "B600"],
            ["barre", "B600"],
            ["Burroughs", "B620"],
            ["Burrows", "B620"],
            ["C.I.A.", "C000"],
            ["coöp", "C100"],
            ["d-day", "D000"],
            ["d jay", "D200"],
            ["de la Rosa", "D462"],
            ["Donnell", "D540"],
            ["Dracula", "D624"],
            ["Drakula", "D624"],
            ["Du Pont", "D153"],
            ["Ekzampul", "E251"],
            ["example", "E251"],
            ["Ellery", "E460"],
            ["Euler", "E460"],
            ["F.B.I.", "F000"],
            ["Gauss", "G200"],
            ["Ghosh", "G200"],
            ["Gutierrez", "G362"],
            ["he", "H000"],
            ["Heilbronn", "H416"],
            ["Hilbert", "H416"],
            ["Jackson", "J250"],
            ["Johnny", "J500"],
            ["Jonny", "J500"],
            ["Kant", "K530"],
            ["Knuth", "K530"],
            ["Ladd", "L300"],
            ["Llyod", "L300"],
            ["Lee", "L000"],
            ["Lissajous", "L222"],
            ["Lukasiewicz", "L222"],
            ["naïve", "N100"],
            ["Miller", "M460"],
            ["Moses", "M220"],
            ["Moskowitz", "M232"],
            ["Moskovitz", "M213"],
            ["O'Conner", "O256"],
            ["O'Connor", "O256"],
            ["O'Hara", "O600"],
            ["O'Mally", "O540"],
            ["Peters", "P362"],
            ["Peterson", "P362"],
            ["Pfister", "P236"],
            ["R2-D2", "R300"],
            ["rÄ≈sumÅ∙", "R250"],
            ["Robert", "R163"],
            ["Rupert", "R163"],
            ["Rubin", "R150"],
            ["Soundex", "S532"],
            ["sownteks", "S532"],
            ["Swhgler", "S246"],
            ["'til", "T400"],
            ["Tymczak", "T522"],
            ["Uhrbach", "U612"],
            ["Van de Graaff", "V532"],
            ["VanDeusen", "V532"],
            ["Washington", "W252"],
            ["Wheaton", "W350"],
            ["Williams", "W452"],
            ["Woolcock", "W422"],
        ]

    def testOne(self):
        for list in self.testList:
            self.assertEqual(count_soundex(list[0]), list[1])

    def tearDown(self):
        del self.testList


def main():
    unittest.main()

if __name__ == '__main__':
    main()