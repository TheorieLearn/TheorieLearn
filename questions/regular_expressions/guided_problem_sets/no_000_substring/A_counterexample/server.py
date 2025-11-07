import re
from typing import Optional, Tuple

import prairielearn as pl
from theorielearn.shared_utils import grade_question_parameterized


def grade(data: pl.QuestionData) -> None:
    def grade_ans(student_ans: str) -> Tuple[bool, Optional[str]]:
        if bool(re.fullmatch("((0|00)11*)*", student_ans)) != bool(
            re.fullmatch("1*((0|00)11*)*(|0|00)", student_ans)
        ):
            return True, None
        return False, None

    grade_question_parameterized(data, "ans", grade_ans)
    pl.set_weighted_score_data(data)
