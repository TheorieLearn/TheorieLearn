NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    block_lengths = [len(s) for s in x.split("1") if len(s) != 0]
    return sum(l % 2 == 0 for l in block_lengths) == sum(
        l % 2 == 1 for l in block_lengths
    )
