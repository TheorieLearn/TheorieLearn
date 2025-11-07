from typing import Any

import prairielearn as pl
import theorielearn.shared_utils as su
import sympy


def grade(data: su.QuestionData) -> None:
    def grade_high1(student_ans: dict[str, Any]) -> tuple[bool, str | None]:
        n = sympy.var("n")
        correct = n + 1
        almost_correct = n
        student_ans_sympy = pl.from_json(student_ans)
        if student_ans_sympy == correct:
            return True, None
        if student_ans_sympy == almost_correct:
            return (
                False,
                "Your upper bound ignores the case where Burr has no jobs left!",
            )
        return False, None

    su.grade_question_parameterized(data, "high1", grade_high1)
    pl.set_weighted_score_data(data)
