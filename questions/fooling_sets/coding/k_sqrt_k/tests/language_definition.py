from math import ceil, sqrt

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    n = len(x)
    k = 1
    while ceil(k * sqrt(k)) < n:
        k += 1
    return ceil(k * sqrt(k)) == n
