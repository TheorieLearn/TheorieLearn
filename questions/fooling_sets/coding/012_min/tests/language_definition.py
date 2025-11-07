import re

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    pattern = "(0*)(1*)(2*)"
    match = re.compile(pattern).fullmatch(x)

    if match is None:
        return False

    i = len(match.group(1))
    j = len(match.group(2))
    k = len(match.group(3))
    return k >= min(i, j)
