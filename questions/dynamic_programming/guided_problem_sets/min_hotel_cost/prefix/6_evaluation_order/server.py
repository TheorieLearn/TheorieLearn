from typing import Any

import prairielearn as pl
from theorielearn.shared_utils import QuestionData, grade_question_parameterized


def grade(data: QuestionData) -> None:
    block_dict = {
        1: "For $i$, in increasing order:",
        2: "For $i$, in decreasing order:",
        3: "Compute $MinCost(i)$",
    }

    def grade_proof(proof: list[Any]):
        if proof[0]["indent"] != 0:
            return (0, "Your first block is indented too far.")
        if proof[0]["inner_html"] == block_dict[3]:
            return (0, "You haven't defined an evaluation order first.")
        if proof[0]["inner_html"] == block_dict[2]:
            return (
                0,
                "Evaluating in decreasing order violates $i-1$ or $i-2$ dependencies.",
            )

        if len(proof) == 1:
            return (0, "Your evaluation is incomplete.")

        if proof[1]["indent"] != 1:
            return (0.33, "Your second block is indented incorrectly.")
        if proof[1]["inner_html"] == block_dict[2]:
            return (
                0.33,
                "Evaluating in decreasing order violates $i-1$ or $i-2$ dependencies.",
            )
        if proof[1]["inner_html"] != block_dict[3]:
            return (
                0.66,
                "You haven't computed $MinCost(i)$ yet.",
            )

        if len(proof) > 2:
            return (0, "Your evaluation is too long.")

        return (1, "Correct!")

    #use the shared grading helper
    grade_question_parameterized(data, "eval", grade_proof, 1, "feedback")
    pl.set_weighted_score_data(data)
