import math

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    n = math.ceil(math.sqrt(2 * len(x)))
    return x == "0" * (n * (n - 1) // 2)
