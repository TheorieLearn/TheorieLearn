import re

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    pattern = "(0*)"
    match = re.compile(pattern).fullmatch(x)

    if match is None:
        return False

    i = len(match.group(1))
    return round(i ** (1 / 3)) ** 3 == i
