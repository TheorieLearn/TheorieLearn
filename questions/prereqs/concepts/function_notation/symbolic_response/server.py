import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from sympy import latex
from theorielearn.sympy_utils.utils import make_random_function


def generate(data: QuestionData) -> None:
    recursive_form, expanded_form, base_expr = make_random_function(
        target_complexity=1.1,
        max_exponential=3,
    )

    data["params"]["base_expr"] = latex(base_expr)
    data["params"]["expr_recursive_form"] = latex(recursive_form)
    data["correct_answers"]["expr_expanded_form"] = pl.to_json(expanded_form)
