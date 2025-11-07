from typing import List

import theorielearn.shared_utils as su
from theorielearn.greedy.greedy_utils import (
    get_advertisers,
    grade_advertisers,
    parse_advertiser_inputs,
)


def parse(data: su.QuestionData) -> None:
    parse_advertiser_inputs(data, ["n", "W"], ["L", "P", "X_w", "X_c"])


def grade(data: su.QuestionData) -> None:
    def get_wrong_X(n: int, W: float, L: List[float], P: List[float]) -> List[float]:
        # use the wrong strategy to compute X_w
        return get_advertisers(n, W, L, P, lambda x: x[1])

    grade_advertisers(data, get_wrong_X)
