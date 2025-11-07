import re

import prairielearn as pl
import sympy as sp
import theorielearn.shared_utils as su


def grade(data: su.QuestionData) -> None:
    def grade_q2(student_ans: str) -> tuple[bool, str | None]:
        sanitized = student_ans.strip()

        sanitized = re.sub(r"(\d)([eE])", r"\1*\2", sanitized)
        sanitized = sanitized.replace("e", "M").replace("E", "M")

        M, V = sp.symbols("M V")

        try:
            student_expr = sp.sympify(sanitized, locals={"M": M, "V": V})
            correct_expr = sp.sympify("8*M + V", locals={"M": M, "V": V})

            if sp.simplify(student_expr - correct_expr) == 0:
                return True, None
            else:
                return (
                    False,
                    "Your expression is not equivalent to the expected answer.",
                )
        except Exception as e:
            return False, f"Could not parse your expression: {e}"

    su.grade_question_parameterized(data, "q2", grade_q2)
    pl.set_weighted_score_data(data)
