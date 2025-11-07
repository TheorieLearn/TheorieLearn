import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"MinCost": 1, "HotelCosts": 1}
    local_variables = {"i", "n"}

    SympyGrader("base0", local_functions, local_variables).grade_question(
        data, "0", "HotelCosts(n)", "HotelCosts(i)"
    )

    SympyGrader("base1", local_functions, local_variables).grade_question(
        data,
        "MinCost(i + 1) + HotelCosts(i)",
        "HotelCosts(i)",
        "HotelCosts(n-1)",
        "MinCost(n) + HotelCosts(n-1)",
        "MinCost(n) + HotelCosts(i)",
        "MinCost(i + 1) + HotelCosts(n-1)",
    )

    pl.set_weighted_score_data(data)
