import prairielearn as pl
from theorielearn.shared_utils import QuestionData, grade_question_tokenized
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"MinCost": 1, "HotelCosts": 1}
    local_variables = {"i", "n"}

    SympyGrader("ans1", local_functions, local_variables).grade_question(
        data, "MinCost(i + 1) + HotelCosts(i)"
    )
    SympyGrader("ans2", local_functions, local_variables).grade_question(
        data, "MinCost(i + 2) + HotelCosts(i)"
    )
    SympyGrader("final", local_functions, local_variables).grade_question(
        data,
        "HotelCosts(i) + min(MinCost(i + 2), MinCost(i + 1))",
        "min(MinCost(i + 2) + HotelCosts(i), MinCost(i + 1) + HotelCosts(i))",
    )

    grade_question_tokenized(data, "base", "n, n-1")

    pl.set_weighted_score_data(data)
