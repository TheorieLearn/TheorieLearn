import re

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x: str) -> bool:
    pattern = "(0*)(1)(0*)"
    match = re.compile(pattern).fullmatch(x)

    if match is None:
        return False

    i = len(match.group(1))
    j = len(match.group(3))

    if j == 0:
        return i == 0

    return i % j == 0
