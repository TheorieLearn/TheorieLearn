from theorielearn.shared_utils import has_no_leading_palindrome

NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x: str) -> bool:
    return has_no_leading_palindrome(x, 3) and (x.count("0") + x.count("1") == len(x))
