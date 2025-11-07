import re

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    pattern = "(0*)(1*)(0*)"
    match = re.compile(pattern).fullmatch(x)

    if match is None:
        return False

    p = len(match.group(1))
    q = len(match.group(2))
    r = len(match.group(3))
    return r == p + q
