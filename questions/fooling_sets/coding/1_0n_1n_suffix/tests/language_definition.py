NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x: str) -> bool:
    def has_correct_suffix(string: str) -> bool:
        n = len(string) // 2
        for length in range(1, n + 1):
            suffix_len = 1 + 2 * length
            actual_suffix = string[-1 * suffix_len :]
            correct_suffix = "1" + "0" * length + "1" * length
            if actual_suffix == correct_suffix:
                return True
        return False

    return has_correct_suffix(x) and (x.count("0") + x.count("1") == len(x))
