import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"MaxFun": 2, "Fun": 1, "sum": 2, "min": 2, "max": 2}
    local_variables = {"v", "c", "Include", "Exclude"}

    SympyGrader("ans1", local_functions, local_variables).grade_question(data, "Fun(v)")

    SympyGrader("ans2", local_functions, local_variables).grade_question(
        data, "MaxFun(c, Exclude)"
    )

    SympyGrader("ans3", local_functions, local_variables).grade_question(
        data, "max( MaxFun(c, Include), MaxFun(c, Exclude) )"
    )

    pl.set_weighted_score_data(data)
