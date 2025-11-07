NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x: str) -> bool:
    def count_leading_zeroes(s: str) -> int:
        res = 0
        for char in s:
            if char == "0":
                res += 1
            else:
                break
        return res

    a = count_leading_zeroes(x)
    c = count_leading_zeroes(x[::-1])
    w_len = len(x) - a - c - 2
    if c + 1 > len(x):
        return False

    one_after_0a = x[a] == "1"
    one_before_0c = x[-1 * c - 1] == "1"
    ones_are_different = a + c + 2 <= len(x)
    only_1s_and_0s = x.count("0") + x.count("1") == len(x)
    lang_cond1 = a <= w_len + c
    lang_cond2 = w_len <= a + c or c <= a + w_len

    return all(
        [
            one_after_0a,
            one_before_0c,
            ones_are_different,
            only_1s_and_0s,
            lang_cond1,
            lang_cond2,
        ]
    )
