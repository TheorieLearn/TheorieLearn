import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"MinMinutes": 3, "TimeNeeded": 1}
    local_variables = {"i", "j", "k", "n", "p"}

    SympyGrader("skipfull", local_functions, local_variables).grade_question(
        data, "MinMinutes(i, j+1, 0)"
    )

    SympyGrader("ansfull", local_functions, local_variables).grade_question(
        data, "TimeNeeded(j) + MinMinutes(i-k-1, j+1, k+1)"
    )

    SympyGrader("final", local_functions, local_variables).grade_question(
        data, "min(TimeNeeded(j) + MinMinutes(i-k-1, j+1, k+1), MinMinutes(i, j+1, 0))"
    )

    pl.set_weighted_score_data(data)
