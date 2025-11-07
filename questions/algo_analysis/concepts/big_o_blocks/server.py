import random
from typing import TypedDict

import prairielearn as pl


class FormulaRankDict(TypedDict):
    "A class with type signatures for the formula rank dict"

    formula: str
    rank: int


def generate(data: pl.QuestionData) -> None:
    # options is a list of (formula, rank) pairs, where ranks indicate relative growth order.
    # Ranks do NOT need to be consecutive.
    options: list[FormulaRankDict] = [
        # ——— subpolynomial ———
        {"formula": "1", "rank": 1},
        {"formula": "100^{100!}", "rank": 1},
        {"formula": "\\log\\log n", "rank": 2},
        {"formula": "\\sqrt{\\lg n}", "rank": 3},
        {"formula": "\\lg n", "rank": 5},
        {"formula": "374\\lg n", "rank": 5},
        {"formula": "\\log (374 n)", "rank": 5},
        {"formula": "\\log_{374} n", "rank": 5},
        {"formula": "\\log (n^{374})", "rank": 5},
        {"formula": "\\log^2 n", "rank": 6},
        {"formula": "\\log^{374} n", "rank": 8},
        # ——— polynomial O(n) ———
        {"formula": "n^{1/374}", "rank": 10},
        {"formula": "\\lfloor \\sqrt{n} \\rfloor", "rank": 12},
        {"formula": "\\lceil \\sqrt{n} \\rceil", "rank": 12},
        {"formula": "2^{\\log_3 n}", "rank": 13},
        {"formula": "n^{\\log_3 2}", "rank": 14},
        {"formula": r"n/\lg n", "rank": 19},
        {"formula": "n", "rank": 20},
        {"formula": "37n + 4", "rank": 20},
        {"formula": "3n - 74", "rank": 20},
        {"formula": "2^{\\lg n}", "rank": 20},
        {"formula": "\\lfloor n/10 \\rfloor", "rank": 20},
        # ——— superlinear polynomial ———
        {"formula": r"n\log n", "rank": 21},
        {"formula": r"n\log^2 n", "rank": 22},
        {"formula": "3^{\\lg n}", "rank": 23},
        {"formula": "n^{\\lg 3}", "rank": 23},
        {"formula": "n^2", "rank": 26},
        {"formula": "4^{\\lg n}", "rank": 26},
        {"formula": r"n^2\log n", "rank": 27},
        {"formula": "n^3", "rank": 28},
        {"formula": "n^{374}", "rank": 29},
        # ——— superpolynomial ———
        {"formula": r"(\lg n)^{\lg n}", "rank": 30},
        {"formula": "n^{\\lg n}", "rank": 31},
        {"formula": "1.00001^n", "rank": 32},
        {"formula": "2^n", "rank": 34},
        {"formula": r"n\cdot 2^n", "rank": 35},
        {"formula": "e^n", "rank": 36},
        {"formula": "3^n", "rank": 37},
        {"formula": "374^n", "rank": 38},
        {"formula": "(\\lg n)^n", "rank": 40},
        {"formula": "n!", "rank": 50},
        {"formula": "n^n", "rank": 60},
    ]

    num_items = 10  # how many options to choose

    # make the ranks consecutive for pl-order-blocks
    data["params"]["functions"] = random.sample(options, num_items)
