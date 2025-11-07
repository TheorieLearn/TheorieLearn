NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    if "#" not in x:
        return False
    m = x.index("#")
    return m == len(x) - m - 1
