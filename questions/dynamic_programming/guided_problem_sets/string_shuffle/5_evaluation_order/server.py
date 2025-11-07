from typing import Any

import prairielearn as pl
from theorielearn.shared_utils import QuestionData, grade_question_parameterized


def grade(data: QuestionData) -> None:
    # Proof blocks omit their tags if they aren't correctly indented.
    # We use this to determine which block we're talking about.
    block_dict = {
        1: "For $i$, in increasing order:",
        2: "For $j$, in increasing order:",
        3: "For $i$, in decreasing order:",
        4: "For $j$, in decreasing order:",
        5: "Compute $ValidShuffle(i,j)$",
    }

    def grade_proof(proof: list[Any]):
        # Check that the first proof block is an increasing evaluation order.
        if proof[0]["indent"] != 0:
            return (0, "Your first block is indented too far.")
        if proof[0]["inner_html"] == block_dict[5]:
            return (0, "You haven't defined an evaluation order first.")
        if proof[0]["inner_html"] in {block_dict[3], block_dict[4]}:
            return (
                0,
                "Evaluating in decreasing order violates $i-1$ or $j-1$ in the recursive definition.",
            )
        # Determine if they used i or j increasing first.
        i_first = proof[0]["inner_html"] == block_dict[1]
        if len(proof) == 1:
            return (0, "Your evaluation is incomplete.")
        # Determine if the second proof block is correct.
        if proof[1]["indent"] != 1:
            return (0.33, "Your second block is indented incorrectly.")
        if proof[1]["inner_html"] in {block_dict[3], block_dict[4]}:
            return (
                0.33,
                "Evaluating in decreasing order violates $i-1$ or $j-1$ in the recursive definition.",
            )
        if proof[1]["inner_html"] == block_dict[5]:
            return (
                0.33,
                f"You haven't defined an evaluation order for {'j' if i_first else 'i'}.",
            )
        if len(proof) == 2:
            return (0, "Your evaluation is incomplete.")
        # We check for length earlier, so either they used the evaluation block or they didn't.
        if proof[2]["indent"] != 2:
            return (0.66, "Your third block is indented incorrectly.")
        if len(proof) > 3:
            return (0, "Your evaluation is too long.")
        if proof[2]["inner_html"] != block_dict[5]:
            return (0.66, "You never evaluate the subproblem.")
        return (1, "Correct!")

    grade_question_parameterized(data, "eval", grade_proof, 1, "feedback")
    pl.set_weighted_score_data(data)
