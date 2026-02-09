import random


def generate(data):
    """
    T(n) = T(n-1) + (an+b)
    T(0) = c

    T(n) = c + an(n+1)/2 + bn
         = O(n) if a == 0 else O(n^2)
    """

    a = random.randint(0, 1) * random.randint(1, 9)
    b = random.randint(2, 9)
    c = random.randint(2, 9)

    rec = "T(n) = \\begin{{cases}} {0} & \\text{{if }} n = 0 \\\\ T(n-1) {1}+{2} & \\text{{otherwise}} \\end{{cases}}".format(
        c, "+{}n".format(a if a > 1 else "") if a > 0 else "", b
    )

    data["params"]["rec"] = rec
    data["params"]["n"] = True if a == 0 else False
