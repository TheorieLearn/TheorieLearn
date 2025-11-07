import re
from typing import Any, Dict, Optional, Tuple

import prairielearn as pl
import theorielearn.shared_utils as su
from theorielearn.FA_coding.incorrect_dfa_for_0100 import fa as dfa

INVALID_FORMAT_FEEDBACK = (
    'Your input should either be "none", "e", '
    "or a non-empty string containing only 0s and 1s."
)


def generate(data: pl.QuestionData) -> None:
    data["params"]["dfa"] = dfa.show_diagram().string()


def grade(data: pl.QuestionData) -> None:
    invalid_input = lambda st: (not bool(re.fullmatch("[01]+", st))) and st not in {
        "none",
        "e",
    }
    target_substring = "0100"

    def grade_notinl(student_ans: str) -> Tuple[bool, Optional[str]]:
        if invalid_input(student_ans):
            raise ValueError(INVALID_FORMAT_FEEDBACK)

        if student_ans == "none":
            return True, None
        else:
            if student_ans == "e":
                student_ans = ""

            if target_substring in student_ans:
                return False, "Your input is in the language."
            elif not dfa.accepts_input(student_ans):
                return False, "The DFA rejects your input"
            else:
                return False, None

    def grade_inl(student_ans: str) -> Tuple[bool, Optional[str]]:
        if invalid_input(student_ans):
            raise ValueError(INVALID_FORMAT_FEEDBACK)

        if student_ans == "none":
            return False, "Not quite, try looking again."
        else:
            if student_ans == "e":
                student_ans = ""

            if not dfa.accepts_input(student_ans):
                if target_substring in student_ans:
                    return True, None
                else:
                    return False, "Your input is not in the language"
            else:
                return False, "The DFA accepts your input"

    su.grade_question_parameterized(data, "notinl", grade_notinl)
    su.grade_question_parameterized(data, "inl", grade_inl)
    pl.set_weighted_score_data(data)
