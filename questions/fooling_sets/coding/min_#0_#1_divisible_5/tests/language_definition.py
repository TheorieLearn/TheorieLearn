NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x: str) -> bool:
    zero_count = x.count("0")
    one_count = x.count("1")
    count_min = min(zero_count, one_count)
    only_zeroes_and_ones = zero_count + one_count == len(x)

    return (count_min % 5) == 0 and only_zeroes_and_ones
