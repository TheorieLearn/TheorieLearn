import re

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x: str) -> bool:
    pattern = "([a-b]*)(c)(d*)"
    match = re.compile(pattern).fullmatch(x)

    if match is None:
        return False

    count_a_in_w = match.group(1).count("a")
    len_d = len(match.group(3))
    return count_a_in_w == len_d
