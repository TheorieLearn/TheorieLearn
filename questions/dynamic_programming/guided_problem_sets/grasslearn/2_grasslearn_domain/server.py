from typing import Any

import prairielearn as pl
import theorielearn.shared_utils as su
import sympy


def grade(data: su.QuestionData) -> None:
    def grade_highk(student_ans: dict[str, Any]) -> tuple[bool, str | None]:
        n = sympy.var("n")
        correct = n - 1
        almost_correct = n
        student_ans_sympy = pl.from_json(student_ans)
        if student_ans_sympy == correct:
            return True, None
        if student_ans_sympy == almost_correct:
            return (
                False,
                "Your upper bound for $k$ could be tighter! Think about your streak length at question $m$, if you've answered every other question correctly.",
            )
        return False, None


    su.grade_question_parameterized(data, "highk", grade_highk)
    pl.set_weighted_score_data(data)
