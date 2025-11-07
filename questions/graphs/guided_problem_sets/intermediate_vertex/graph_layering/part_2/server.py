import prairielearn as pl
from theorielearn.shared_utils import QuestionData, grade_question_tokenized


def grade(data: QuestionData) -> None:
    grade_question_tokenized(data, "nodes", "{0, 1}")
    pl.set_weighted_score_data(data)
