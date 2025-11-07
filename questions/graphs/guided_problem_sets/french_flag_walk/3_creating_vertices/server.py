from typing import Any, Dict

import prairielearn as pl
from theorielearn.shared_utils import grade_question_tokenized


def grade(data: pl.QuestionData) -> None:
    grade_question_tokenized(data, "nodes", "{0,1,2}")
    pl.set_weighted_score_data(data)
