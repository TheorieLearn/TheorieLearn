def generateLanguage(max_length):
    """Strings over {0,1} with equal numbers of 0s and 1s."""
    result = set()
    for length in range(0, max_length + 1, 2):  # only even lengths
        for bits in range(2**length):
            s = bin(bits)[2:].zfill(length) if length > 0 else ""
            if s.count("0") == s.count("1"):
                result.add(s)
    return result
