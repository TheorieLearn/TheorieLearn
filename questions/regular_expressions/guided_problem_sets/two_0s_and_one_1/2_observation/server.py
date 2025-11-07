from typing import Any, Dict, Optional

import prairielearn as pl
from theorielearn.shared_utils import set_holistic_feedback


def grade(data: pl.QuestionData) -> None:
    def feedback_function(p1: str, p2: str, p3: str) -> Optional[str]:
        thing_contained = f"a {p1} with {p2} two 0s and {p3} one 1"

        if p2 == "greater than":
            return f"Would strings in the language which have exactly two 0s contain {thing_contained}?"
        elif p3 == "greater than":
            return f"Would strings in the language which have exactly one 1 contain {thing_contained}?"
        elif p2 == "less than":
            return f"Are strings containing {thing_contained} guaranteed to have enough 0s to be in the language?"
        elif p3 == "less than":
            return f"Are strings containing {thing_contained} guaranteed to have enough 1s to be in the language?"
        elif p1 == "substring":
            return 'Consider the counterexample "01110" and review the substring and subsequence definitions.'

        return None

    pl.set_all_or_nothing_score_data(data)
    set_holistic_feedback(data, "feedback", feedback_function)
