import re

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x: str) -> bool:
    pattern = "0*"
    match = re.compile(pattern).fullmatch(x)
    if match is None:
        return False

    if x == "":
        return True

    n = len(x)
    for j in range(n):
        i = j * j
        if i + j == n:
            return True
        elif i + j > n:
            return False

    return False
