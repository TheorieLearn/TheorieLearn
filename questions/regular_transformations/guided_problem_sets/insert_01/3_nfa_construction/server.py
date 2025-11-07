from typing import Any, Dict

import prairielearn as pl
from theorielearn.shared_utils import grade_question_tokenized


def grade(data: pl.QuestionData) -> None:
    for question_name in data["correct_answers"].keys():
        grade_question_tokenized(data, question_name)
    pl.set_weighted_score_data(data)
