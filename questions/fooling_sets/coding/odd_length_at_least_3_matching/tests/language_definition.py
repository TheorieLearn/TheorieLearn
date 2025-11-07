import math

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    if len(x) % 2 != 1 or len(x) < 3:
        return False

    mid = math.ceil(len(x) / 2) - 1

    return x[0] == x[mid] == x[-1]
