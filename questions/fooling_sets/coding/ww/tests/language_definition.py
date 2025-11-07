NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    h = len(x) // 2
    return x[:h] == x[h:]
