NUM_ELEMENTS_TO_CHECK = 50

a, b = 1, 2
fib_numbers = {a, b}


def isInLanguage(x):
    if x.count("0") != len(x):
        return False

    global a, b
    while b < len(x):
        a, b = b, a + b
        fib_numbers.add(b)

    return len(x) in fib_numbers
