NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x: str) -> bool:
    return (
        x == x[::-1] and (len(x) % 3 == 0) and (x.count("0") + x.count("1") == len(x))
    )
