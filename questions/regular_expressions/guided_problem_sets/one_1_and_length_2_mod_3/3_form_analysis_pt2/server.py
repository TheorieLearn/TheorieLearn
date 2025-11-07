from typing import Any, Dict, Optional, Tuple

import numpy as np
import prairielearn as pl
from theorielearn.shared_utils import grade_question_parameterized


def grade(data: pl.QuestionData) -> None:
    pair1 = [1, 0]
    pair2 = [0, 1]
    pair3 = [2, 2]

    expected_ans = [pair1, pair2, pair3]

    def grade_ordered_pairs(student_ans: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        # Convert student input
        ans = np.array(student_ans["_value"]).tolist()

        # Check for formatting errors
        for pair in ans:
            if not all(type(x) is int for x in pair):
                raise ValueError(
                    "Your inputs should all be integers. Please refer to the example in the problem statement."
                )
            if not all(x in {0, 1, 2} for x in pair):
                raise ValueError(
                    "You should only consider values in the interval [0, 2]."
                )

        # np.array must be uniformly shaped
        if len(ans[0]) != 2:
            raise ValueError(
                "Your input is incorrectly formatted. Please refer to the example in the problem statement."
            )

        # Check for correct case
        if len(ans) == 3 and all(a in ans for a in expected_ans):
            return True, None
        # Otherwise, give feedback for wrong answers
        elif pair1 not in ans and pair2 not in ans:
            return (
                False,
                "Review some example strings in the language that you picked out in part one of this guided question. What were the values of x and y there?",
            )
        elif pair1 in ans and pair2 not in ans:
            return (
                False,
                'It looks like you covered the case "00001", but what about the reversal of that string?',
            )
        elif pair1 not in ans and pair2 in ans:
            return (
                False,
                'It looks like you covered the case "10000", but what about the reversal of that string?',
            )
        elif pair3 not in ans:
            return False, 'Consider the case "00100". Does your answer cover this?'
        else:  # len(ans) > 3:
            return False, "It looks like you may have some redundant cases."

    grade_question_parameterized(data, "ordered_pairs", grade_ordered_pairs)

    pl.set_weighted_score_data(data)
