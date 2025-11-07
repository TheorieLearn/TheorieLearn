from typing import Any, Dict, Optional, Tuple

import prairielearn as pl
from theorielearn.shared_utils import grade_question_parameterized, is_perfect_power


def grade(data: pl.QuestionData) -> None:
    i = data["submitted_answers"]["i"]
    j = data["submitted_answers"]["j"]

    def grade_proof(student_ans: int) -> Tuple[bool, Optional[str]]:
        if i == j or i < 0 or j < 0:
            return (False, "$i$ and $j$ must be two distinct non-negative integers!")
        elif not is_perfect_power(j**2 + 2 * i + 1, 2):
            first_string_expanded = (
                f"$0^{{i^{{2}} + 2i + 1}} = 0^{{{str(i**2 + 2 * i + 1)}}}$"
            )
            second_string_expanded = (
                f"$0^{{j^{{2}} + 2i + 1}} = 0^{{{str(j**2 + 2*i + 1)}}}$"
            )
            return (
                False,
                f"{first_string_expanded} is accepted by the language, but {second_string_expanded} is not.",
            )
        return (True, None)

    grade_question_parameterized(data, "i", grade_proof)
    grade_question_parameterized(data, "j", grade_proof, feedback_field_name="feedback")
    pl.set_weighted_score_data(data)
