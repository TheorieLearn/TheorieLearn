import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"MinCost": 1, "HotelCosts": 1}
    local_variables = {"i", "n"}

    SympyGrader("base1", local_functions, local_variables).grade_question(
        data, "0", "HotelCosts(1)", "HotelCosts(i)"
    )

    SympyGrader("base2", local_functions, local_variables).grade_question(
        data,
        "MinCost(i - 1) + HotelCosts(i)",
        "HotelCosts(i)",
        "HotelCosts(2)",
        "MinCost(1) + HotelCosts(2)",
        "MinCost(1) + HotelCosts(i)",
        "MinCost(i - 1) + HotelCosts(2)",
    )

    pl.set_weighted_score_data(data)
