from typing import Any, Dict, Optional

import prairielearn as pl
from theorielearn.shared_utils import set_holistic_feedback


def grade(data: pl.QuestionData) -> None:
    def feedback_function(q1: str, q2: str, q3: int, q4: str) -> Optional[str]:
        if q1 == "1s":
            return "Are you sure there should be a restriction on the length of 1-runs?"
        elif q4 == "0s":
            return "Are you sure there's no restriction on the length of 0-runs?"
        elif q2 == "not equal to":
            return (
                "Are you sure there's only one length that is not allowed for 0-runs?"
            )
        elif q2 == "exactly":
            return (
                "Are you sure that there's only one length that is allowed for 0-runs?"
            )
        elif q2 == "at least":
            return (
                f"Are you sure that a 0-run of length {max(q3, 100)} should be allowed?"
            )
        elif q3 < 2:
            return "Are you sure a 0-run of length 2 should not be allowed?"
        elif q3 > 2:
            return f"Are you sure that a 0-run of length {q3} should be allowed?"
        else:
            return None

    pl.set_all_or_nothing_score_data(data)
    set_holistic_feedback(data, "feedback", feedback_function, hide_partial_scores=True)
