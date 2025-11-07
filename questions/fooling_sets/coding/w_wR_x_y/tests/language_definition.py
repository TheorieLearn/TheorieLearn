NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x: str) -> bool:
    max_w_len = (len(x) - 2) // 2

    def possible_w():
        for w_len in range(1, max_w_len + 2):
            if (2 * w_len) + 2 > len(x):
                continue
            w = x[:w_len]
            w_r = x[w_len : w_len * 2][::-1]
            if w == w_r:
                return True
        return False

    return possible_w() and (x.count("0") + x.count("1") == len(x))
