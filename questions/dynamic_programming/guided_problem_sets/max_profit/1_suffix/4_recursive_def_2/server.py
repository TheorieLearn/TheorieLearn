import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"MaxProfit": 1, "profit": 1, "skip": 1}
    local_variables = {"i", "n"}

    SympyGrader("ans1", local_functions, local_variables).grade_question(
        data, "MaxProfit(i + 1)"
    )

    SympyGrader("ans2", local_functions, local_variables).grade_question(
        data, "profit(i) + MaxProfit(i + skip(i) + 1)"
    )

    SympyGrader("final", local_functions, local_variables).grade_question(
        data, "max(MaxProfit(i + 1), profit(i) + MaxProfit(i + skip(i) + 1))"
    )

    SympyGrader("base_ans", local_functions, local_variables).grade_question(data, "0")

    pl.set_weighted_score_data(data)
