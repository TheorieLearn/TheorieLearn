import prairielearn as pl
from theorielearn.shared_utils import QuestionData, grade_question_tokenized
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"MinCost": 2, "HotelCosts": 1}
    local_variables = {"i", "n", "j", "k"}

    SympyGrader("ans1", local_functions, local_variables).grade_question(
        data, "MinCost(i + 1, j) + HotelCosts(i)"
    )
    SympyGrader("ans2", local_functions, local_variables).grade_question(
        data, "MinCost(i + 2, j) + HotelCosts(i)"
    )
    SympyGrader("ans3", local_functions, local_variables).grade_question(
        data, "MinCost(i + 1, j - 1)"
    )
    SympyGrader("ans4", local_functions, local_variables).grade_question(
        data, "MinCost(i + 2, j - 1)"
    )

    SympyGrader("final", local_functions, local_variables).grade_question(
        data,
        "min(HotelCosts(i) + MinCost(i + 1, j), HotelCosts(i) + MinCost(i + 2, j), MinCost(i + 1, j - 1), MinCost(i + 2, j - 1))",
    )

    grade_question_tokenized(data, "basei", "n - 1, n")
    grade_question_tokenized(data, "basej", "0")

    pl.set_weighted_score_data(data)
