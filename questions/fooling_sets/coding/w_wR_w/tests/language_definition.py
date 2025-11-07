NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x: str) -> bool:
    h = len(x) // 3
    return x[:h] == x[2 * h :] and x[:h] == x[h : 2 * h][::-1]
