from typing import Any
import prairielearn as pl
from theorielearn.shared_utils import QuestionData, grade_question_parameterized

def grade(data: QuestionData) -> None:
    block_dict = {
        1: "For $i$, in decreasing order:",
        2: "For $j$, in increasing order:",
        3: "For $i$, in increasing order:",
        4: "For $j$, in decreasing order:",
        5: "Compute $MinCost(i,j)$",
    }

    def grade_proof(proof: list[Any]):
        if proof[0]["indent"] != 0:
            return (0, "Your first block is indented too far.")
        if proof[0]["inner_html"] == block_dict[5]:
            return (0, "You haven't defined an evaluation order first.")
        if proof[0]["inner_html"] == block_dict[3]:
            return (0, "Evaluating in increasing order violates the suffix dependency on $i+1$ and $i+2$.")
        if proof[0]["inner_html"] == block_dict[4]:
            return (0, "Evaluating in decreasing $j$ order violates $j-1$ dependencies.")

        i_first = proof[0]["inner_html"] in {block_dict[1], block_dict[3]}
        if len(proof) == 1:
            return (0, "Your evaluation is incomplete.")

        if proof[1]["indent"] != 1:
            return (0.33, "Your second block is indented incorrectly.")
        if proof[1]["inner_html"] == block_dict[3]:
            return (0.33, "Evaluating in increasing order violates suffix dependencies on $i+1$ and $i+2$.")
        if proof[1]["inner_html"] == block_dict[4]:
            return (0.33, "Evaluating in decreasing $j$ order violates $j-1$ dependencies.")
        if proof[1]["inner_html"] == block_dict[5]:
            return (0.33, f"You haven't defined an evaluation order for {'j' if i_first else 'i'}.")

        if len(proof) == 2:
            return (0, "Your evaluation is incomplete.")

        if proof[2]["indent"] != 2:
            return (0.66, "Your third block is indented incorrectly.")
        if len(proof) > 3:
            return (0, "Your evaluation is too long.")
        if proof[2]["inner_html"] != block_dict[5]:
            return (0.66, "You never evaluate the subproblem.")

        return (1, "Correct!")

    grade_question_parameterized(data, "eval", grade_proof, 1, "feedback")
    pl.set_weighted_score_data(data)
