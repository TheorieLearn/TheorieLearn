NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    if "#" not in x:
        return False
    x1, x2 = x.split("#")
    return x1 in x2
