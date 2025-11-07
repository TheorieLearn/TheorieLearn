import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"O": 1, "T": 1}
    local_variables = {"n"}

    grader = SympyGrader("ans", local_functions, local_variables)

    grader.grade_question(data, "O(n) + T(n / 7) + T(5 * n / 7)")
    pl.set_weighted_score_data(data)
