import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"LCS": 2}
    local_variables = {"i", "j", "n", "m"}

    SympyGrader("ans1", local_functions, local_variables).grade_question(
        data, "LCS(i-1, j)"
    )

    SympyGrader("ans2", local_functions, local_variables).grade_question(
        data, "LCS(i, j-1)"
    )

    SympyGrader("ans3", local_functions, local_variables).grade_question(
        data, "1+LCS(i-1, j-1)"
    )

    SympyGrader("expr1_ans", local_functions, local_variables).grade_question(
        data, "max(LCS(i-1, j), LCS(i, j-1))"
    )

    expr2_grader = SympyGrader("expr2_ans", local_functions, local_variables)
    expr2_grader.answer_includes_specific_errors_feedback(
        "1+LCS(i-1,j-1)",
        "It seems like you tried to do a greedy optimization in this definition. Although it is \
        correct in this case, we want to remind you that we require a proof for all greedy optimizations on homeworks \
        and exams. Since there's no way to submit a proof in this assignment, we will only accept the unoptimized solution.",
    )
    expr2_grader.grade_question(data, "max(LCS(i-1, j), LCS(i, j-1), 1+LCS(i-1,j-1))")

    SympyGrader("base_ans", local_functions, local_variables).grade_question(data, "0")

    pl.set_weighted_score_data(data)
