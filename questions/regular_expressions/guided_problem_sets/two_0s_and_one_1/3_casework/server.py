from typing import Any, Dict, Optional, Tuple

import prairielearn as pl
from theorielearn.shared_utils import grade_question_parameterized


def grade(data: pl.QuestionData) -> None:
    # Correct answer definition
    expected_ans = sorted(["001", "010", "100"])

    def grade_input_list(student_ans: str) -> Tuple[bool, Optional[str]]:
        # Format string input to a list of strings
        seqs = [x.strip() for x in student_ans.split(",")]

        # Raise value error in case of invalid characters
        for s in seqs:
            if not all(char in {"0", "1"} for char in s):
                raise ValueError(
                    "There was an issue parsing your list. Make sure to use comma separated values and use only 1 and 0."
                )

        # Sort answers
        seqs.sort()

        # Check for correct answer
        if seqs == expected_ans:
            return True, None
        # Incorrect answer responses
        elif len(seqs) < 3:
            return (
                False,
                "You may be missing some cases. Are there any other possible subsequences?",
            )
        elif len(seqs) > 3:
            return (
                False,
                "You may have some redundant or incorrect subsequences. Re-consider the possible subsequences that would satisfy the constraints of this language.",
            )
        else:
            for s in seqs:
                if len(s) > 3:
                    return (
                        False,
                        f"Does the full subsequence {s} in your answer really need to be present in order to satisfy the constraints of this language?",
                    )
                elif s.count("0") != 2 or s.count("1") != 1:
                    return (
                        False,
                        f"We want to enforce that at least two 0s and at least one 1 are present in any string in this language. The subsequence {s} in your list would fail to enforce this because the subsequence itself should also be a valid string in the language.",
                    )
            return False, "You may have some duplicate subsequences."

    # Call parametrized grading functions

    grade_question_parameterized(data, "subseqs", grade_input_list)

    pl.set_weighted_score_data(data)
