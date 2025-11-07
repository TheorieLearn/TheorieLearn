import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"MinCost": 2, "HotelCosts": 1}
    local_variables = {"i", "n", "j", "k"}

    SympyGrader("base0", local_functions, local_variables).grade_question(
        data, "0", "HotelCosts(n)", "HotelCosts(i)"
    )

    SympyGrader("base1", local_functions, local_variables).grade_question(
        data, "0", "HotelCosts(n)", "HotelCosts(i)"
    )

    SympyGrader("base2", local_functions, local_variables).grade_question(
        data,
        "MinCost(i + 1, j) + HotelCosts(i)",
        "HotelCosts(i)",
        substitutions=[("i", "n - 1"), ("j", "0")],
    )

    SympyGrader("base3", local_functions, local_variables).grade_question(
        data,
        "0",
        "min(MinCost(i + 1, j) + HotelCosts(i), MinCost(i + 1, j - 1))",
        "min(HotelCosts(i), MinCost(i + 1, j - 1))",
        "min(0, MinCost(i + 1, j - 1))",
        "min(MinCost(i + 1, j) + HotelCosts(i), 0)",
        substitutions=[("i", "n - 1")],
    )

    SympyGrader("base4", local_functions, local_variables).grade_question(
        data,
        "min(MinCost(i + 1, j) + HotelCosts(i), MinCost(i + 2, j) + HotelCosts(i))",
        "HotelCosts(i) + min(MinCost(i + 1, j), MinCost(i + 2, j))",
        substitutions=[("j", "0")],
    )

    pl.set_weighted_score_data(data)
