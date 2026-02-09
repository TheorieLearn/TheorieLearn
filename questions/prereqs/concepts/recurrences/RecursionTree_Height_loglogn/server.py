import random


def generate(data):
    b = random.randint(2, 4)
    c = random.randint(1, 5)
    d = random.randint(1, 3)
    q = random.randint(1, 3) if b < 4 else random.randint(1, 2)

    rec = "T(n) = \\begin{{cases}} {0} & \\text{{if }} n \\le 1000 \\\\ {1}T(\\sqrt[{2}]{{n}}) + n{3} & \\text{{otherwise}} \\end{{cases}}".format(
        c, b**q, b, "^{}".format(d) if d > 1 else ""
    )

    data["params"]["rec"] = rec
    # T(n) = c if n <= 1000 and b^q * T(root(n, b)) + n^d otherwise
    data["params"]["b"] = b
    data["params"]["d"] = d if d > 1 and d != b else b+1 # Only used for wrong MCQ answers
