import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"WorldTour": 2, "d": 2}
    local_variables = {"i", "n", "t", "S"}

    SympyGrader("ans1", local_functions, local_variables).grade_question(
        data, "d(i,t) + WorldTour(S - t,t)", "d(t,i) + WorldTour(S - t,t)"
    )

    pl.set_weighted_score_data(data)
