import random

import sympy
from theorielearn.shared_utils import QuestionData
from sympy import latex
from theorielearn.sympy_utils.utils import make_random_function


def generate(data: QuestionData) -> None:
    # use old recursive complexity (all 0.5) to keep the problem's behavior the same
    x = sympy.symbols("x")
    base_expr_pairs = [
        (x**2, 0.5),
        (x + 1, 0.5),
        (2**x, 0.5),
    ]

    recursive_form, expanded_form, base_expr = make_random_function(
        target_complexity=1.2, base_expr_pair_passed=random.choice(base_expr_pairs)
    )

    data["params"]["base_expr"] = latex(base_expr)
    data["params"]["expanded_form"] = latex(expanded_form)
    data["params"]["recursive_form"] = latex(recursive_form)

    incorrect_forms: set[str] = set()
    while len(incorrect_forms) < 6:
        incorrect_forms.add(latex(make_random_function(1.2, (base_expr, 0.5))[0]))
    data["params"]["incorrect_forms"] = list(incorrect_forms)
