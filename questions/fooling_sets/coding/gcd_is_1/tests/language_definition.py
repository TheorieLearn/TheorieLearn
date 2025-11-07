import math

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    m = x.count("0")
    n = x.count("1")
    return x == "0" * m + "1" * n and math.gcd(m, n) == 1
