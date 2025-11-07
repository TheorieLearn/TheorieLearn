from typing import Any, Dict

import prairielearn as pl
from theorielearn.shared_utils import grade_question_tokenized


def generate(data: pl.QuestionData) -> None:
    data["params"]["row_data"] = [
        {"i": 1},
        {"i": 2},
        {"i": 3},
        {"i": 4},
        {"i": 5},
        {"i": 6},
    ]
    maxprofit_correct = [5, 90, 7, 6, 107, 110]
    for i in range(6):
        data["correct_answers"][f"maxprofit_{i}"] = maxprofit_correct[i]


def grade(data: pl.QuestionData) -> None:
    grade_question_tokenized(data, "incorrect_trials", "1, 2, 3")
    grade_question_tokenized(data, "correct_trials", "1, 3")

    pl.set_weighted_score_data(data)
