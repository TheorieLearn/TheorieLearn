NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    num0 = num1 = num01 = num10 = 0

    for symbol in x:
        if symbol == "0":
            num0, num1, num01, num10 = num0 + 1, num1, num01, num10 + num1
        else:
            num0, num1, num01, num10 = num0, num1 + 1, num01 + num0, num10

    return num01 == num10
