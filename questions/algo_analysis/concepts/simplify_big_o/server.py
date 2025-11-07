import random

import prairielearn as pl
from sympy import factorial, latex, log, simplify, sqrt, symbols


def generate(data: pl.QuestionData) -> None:
    n = symbols("n")

    # f1: p11^(n/p12)
    p11, p12 = random.choice([(4, 2), (9, 2), (16, 4), (27, 3), (64, 3), (81, 2)])
    f1 = latex(p11 ** (n / p12))
    g1 = simplify(p11 ** (n / p12))

    # f2: p21^(log_p22(n))
    p21 = random.randint(2, 9)
    p22 = random.randint(2, 9)
    f2 = f"{p21} ^ {{\\log_{p22} n}}"
    g2 = simplify(n ** log(p21, p22))

    # f3: log(n^p3)
    p3 = random.randint(2, 9)
    f3 = latex(log(n**p3))
    g3 = log(n)

    # f4: log(p41 * n^(p42*n))
    p41 = random.randint(2, 9)
    p42 = random.randint(2, 9)
    f4 = latex(log(p41 * n ** (p42 * n)))
    g4 = n * log(n)

    # f5: log(n!)
    f5 = latex(log(factorial(n)))
    g5 = n * log(n)

    # f6: p6*n + n*log(n)
    p6 = random.randint(2, 9)
    f6 = latex(p6 * n + n * log(n))
    g6 = n * log(n)

    # f7: n^p71 + p72*n^p73 + p74
    p71 = random.randint(5, 9)
    p72 = random.randint(20, 50)
    p73 = random.randint(2, 4)
    p74 = random.randint(100, 1000)
    f7 = latex(n**p71 + p72 * n**p73 + p74)
    g7 = n**p71

    # f8: p81^n + p82^n + n^p83, p82 > p81
    p81 = random.randint(2, 4)
    p82 = random.randint(5, 9)
    p83 = random.randint(2, 9)
    f8 = latex(p81**n + p82**n + n**p83)
    g8 = p82**n

    # f9: p9^n + n! + n^n
    p9 = random.randint(2, 9)
    f9 = latex(p9**n + factorial(n) + n**n)
    g9 = n**n

    # f10: loglog(n) + log(n) + sqrt(log(n))
    f10 = latex(log(log(n)) + log(n) + sqrt(log(n)))
    g10 = log(n)

    # randomly choose one variant
    fs = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    gs = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10]
    i = random.randint(0, 9)
    f = fs[i]
    data["params"]["f"] = f
    g = gs[i]
    data["correct_answers"]["f"] = str(g)
