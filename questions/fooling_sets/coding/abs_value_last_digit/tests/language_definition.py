NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    return abs(x.count("0") - x.count("1")) % 10 == 9
