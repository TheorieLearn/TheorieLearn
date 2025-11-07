NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    for i in range(6, len(x) + 1):
        prefix = x[:i]
        if prefix == prefix[::-1]:
            return True

    return False
