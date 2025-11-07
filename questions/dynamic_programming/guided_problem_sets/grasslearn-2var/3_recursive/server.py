import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"MinMinutes": 2, "TimeNeeded": 1, "Points": 1}
    local_variables = {"i", "j", "n", "p"}

    SympyGrader("skipfull", local_functions, local_variables).grade_question(
        data, "MinMinutes(i, j+1)"
    )

    SympyGrader("anspoints", local_functions, local_variables).grade_question(
        data, "i-Points(j)"
    )

    SympyGrader("ansfull", local_functions, local_variables).grade_question(
        data, "TimeNeeded(j) + MinMinutes(i-Points(j), j+1)"
    )

    SympyGrader("final", local_functions, local_variables).grade_question(
        data, "min(TimeNeeded(j) + MinMinutes(i-Points(j), j+1), MinMinutes(i, j+1))"
    )
    pl.set_weighted_score_data(data)
