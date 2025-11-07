from typing import Any, Dict

import prairielearn as pl
from theorielearn.shared_utils import grade_question_tokenized


def grade(data: pl.QuestionData) -> None:
    grade_question_tokenized(data, "nodes", "{None, W, WB}")
    pl.set_weighted_score_data(data)
