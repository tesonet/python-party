# My comments:
1) Thank you for the interesting task.
2) I've chosen my code line length of 99 chars (PEP8).
3) I hope that I've fulfilled your requirements.

# Task for Great Python developer

If you found this task it means we are looking for you!

## Task

### Word Search

Implement a CLI tool that finds phrases in a given text file. Search phrase (single word) can be misspelled. 
Use American Soundex algorithm to match words - https://en.wikipedia.org/wiki/Soundex. 
Software should return the top unique 5 matched words.

Sample file wiki_lt.txt:
```
   Lithuania (UK and US: Listeni/ˌlɪθuːˈeɪniə/,[11][12][13] Lithuanian: Lietuva
   [lʲɪɛtʊˈvɐ]), officially the Republic of Lithuania (Lithuanian: Lietuvos
   Respublika), is a country in Northern Europe.[14] One of the three Baltic
   states, it is situated along the southeastern shore of the Baltic Sea, to the
   east of Sweden and Denmark. It is bordered by Latvia to the north, Belarus to
   the east and south, Poland to the south, and Kaliningrad Oblast (a Russian
   exclave) to the southwest. Lithuania has an estimated population of 2.9 million
   people as of 2015, and its capital and largest city is Vilnius. Lithuanians are
   a Baltic people. The official language, Lithuanian, along with Latvian, is one
   of only two living languages in the Baltic branch of the Indo-European language
   family.
```

Sample usage:

`$ ./find.py wiki_lt.txt lituania`

Sample output:
```
   Lithuania
   Lithuanian
   Lietuva
   Listeni
   living
```
The exact results might be different because of different scoring, matching, sorting algorithms, etc.

NOTE that given text file might be larger than we have RAM on our machine, e.g. +4 GB, etc.
Any parallelized optimizations are encouraged.

## Few simple steps

1. Fork this repo
2. Do your best
3. Prepare pull request and let us know that you are done

## Few simple requirements

- Use Python 3.
- It should be easy to identify candidate's code. It should not be buried inside some framework directory structure.
- Proper error handling must be implemented, user input must be validated.

## Bonus

- The more code is covered with automated tests, the better. Unit, integration, end to end tests, etc. are all encouraged.
- Use [PEP 8 style guide](http://pep8.org/).
- Use pylint, flake8 or any other tool to statically test code.
- Use [mypy type hints](http://www.mypy-lang.org/).
