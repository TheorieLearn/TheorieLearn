import re

NUM_ELEMENTS_TO_CHECK = 10


def isInLanguage(x):
    pattern = "(0*)"
    match = re.compile(pattern).fullmatch(x)

    if match is None:
        return False

    def is_Power_of_three(n: int) -> bool:
        while n % 3 == 0:
            n //= 3
        return n == 1

    return is_Power_of_three(len(x))
