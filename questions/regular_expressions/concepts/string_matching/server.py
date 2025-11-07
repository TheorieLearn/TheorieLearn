import random
import re
from typing import Optional, Tuple

import prairielearn as pl
from theorielearn.shared_utils import QuestionData, grade_question_parameterized

INVALID_FORMAT_FEEDBACK = (
    "Your input should a non-empty string containing only 0s and 1s."
)


def generate(data: QuestionData) -> None:
    # define language
    l1 = "\\{xyx^R \\mid x, y \\in \\Sigma^+\\}"
    l2 = "0^+ (0+1)^+ 0^+ + 1^+ (0+1)^+ 1^+"
    l3 = "\\{w \\mid w = 0^n \\Sigma^* 1^n, n>0\\}"

    # generate string in l1
    possible_x = ["10", "01", "11", "001", "1001", "1101"]
    possible_y = ["10", "01", "11", "001", "1001", "1101"]
    x = random.choice(possible_x)
    y = random.choice(possible_y)
    w1 = x + y + x[::-1]

    # generate string in l2
    possible_x = ["11", "00", "111", "000", "1101"]
    possible_y = ["1", "0", "101", "010", "111"]
    x = random.choice(possible_x)
    y = random.choice(possible_y)
    w2 = x + y + x

    # generate string in l3
    n = random.randint(2, 4)
    y = random.choice(possible_y)
    w3 = "0" * n + y + "1" * n

    # define pattern in string
    p1 = "xyx^R"
    p2 = "xyx"
    p3 = "xy"

    # random generate a variant
    ls = [l1, l2, l3]
    ws = [w1, w2, w3]
    ps = [p1, p2, p3]

    i = random.randint(0, 2)
    data["params"]["l"] = ls[i]
    data["params"]["w"] = ws[i]
    data["params"]["p"] = ps[i]


def grade(data: QuestionData) -> None:
    invalid_input = lambda st: (not bool(re.fullmatch("[01]+", st)))

    x1 = data["submitted_answers"]["x1"]
    y1 = data["submitted_answers"]["y1"]
    x2 = data["submitted_answers"]["x2"]
    y2 = data["submitted_answers"]["y2"]

    w = data["params"]["w"]
    p = data["params"]["p"]

    if p == "xyx^R":
        w1 = x1 + y1 + x1[::-1]
        w2 = x2 + y2 + x2[::-1]
    elif p == "xyx":
        w1 = x1 + y1 + x1
        w2 = x2 + y2 + x2
    elif p == "xy":
        w1 = x1 + y1
        w2 = x2 + y2

    def grade_matching_1(student_ans: str) -> Tuple[bool, Optional[str]]:
        if invalid_input(student_ans):
            raise ValueError(INVALID_FORMAT_FEEDBACK)

        if w1 != w:
            return (
                False,
                f"Incorrect pattern matching for {w}: your matched string is {w1} using {x1} and {y1}.",
            )

        return (True, None)

    def grade_matching_2(student_ans: str) -> Tuple[bool, Optional[str]]:
        if invalid_input(student_ans):
            raise ValueError(INVALID_FORMAT_FEEDBACK)

        if w2 != w:
            return (
                False,
                f"Incorrect pattern matching for {w}: your matched string is {w2} using {x2} and {y2}.",
            )
        elif x1 == x2 and y1 == y2:
            return (False, "your second example must be distinct from the first one!")

        return (True, None)

    grade_question_parameterized(data, "x1", grade_matching_1)
    grade_question_parameterized(data, "y1", grade_matching_1)
    grade_question_parameterized(data, "x2", grade_matching_2)
    grade_question_parameterized(data, "y2", grade_matching_2)
    pl.set_weighted_score_data(data)
