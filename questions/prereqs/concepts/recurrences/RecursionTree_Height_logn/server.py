import random


def generate(data):
    b = random.randint(2, 4)
    c = random.randint(1, 5)
    d = random.randint(1, 3)
    p = random.randint(0, 3) if b < 4 else random.randint(0, 2)
    q = random.randint(1, 3) if b < 4 else random.randint(1, 2)

    rec = "T(n) = \\begin{{cases}} {0} & \\text{{if }} n = {1} \\\\ {2}T(\\frac{{n}}{{{3}}}) + n{4} & \\text{{otherwise}} \\end{{cases}}".format(
        c, b**p, b**q, b, "^{}".format(d) if d > 1 else ""
    )

    data["params"]["rec"] = rec
    # T(n) = c if n = b^p and b^q * T(n/b) + n^d otherwise
    data["params"]["b"] = b
    data["params"]["d"] = d if d > 1 and d != b else b+1 # Only used for wrong MCQ answers
    data["params"]["btp"] = b**p
