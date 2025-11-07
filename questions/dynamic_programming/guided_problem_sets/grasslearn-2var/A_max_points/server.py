import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"MaxPoints": 2, "TimeNeeded": 1, "Points": 1}
    local_variables = {"i", "j", "n", "m"}

    SympyGrader("skipfull", local_functions, local_variables).grade_question(
        data, "MaxPoints(i, j+1)"
    )

    SympyGrader("ansfull", local_functions, local_variables).grade_question(
        data, "Points(j) + MaxPoints(i-TimeNeeded(j), j+1)"
    )

    pl.set_weighted_score_data(data)
