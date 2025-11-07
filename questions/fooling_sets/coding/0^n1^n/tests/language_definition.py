NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    if len(x) % 2 != 0:
        return False

    n = len(x) // 2
    return x == "0" * n + "1" * n
