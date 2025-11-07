from typing import Optional

import prairielearn as pl
import theorielearn.scaffolded_writing.scaffolded_graph_utils as sw_gu
from theorielearn.scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from theorielearn.scaffolded_writing.graph_cfgs import get_ham_path_cycle_cfg
from theorielearn.shared_utils import QuestionData


def avoid_additional_restrictions(
    submission: sw_gu.GraphStudentSubmission,
) -> Optional[str]:
    if submission.does_path_exist("ADDITIONAL_RESTRICTION", "of the same length"):
        return "Why should we require that the Hamiltonian cycle and Hamiltonian path have the same length?"
    if submission.does_path_exist(
        "ADDITIONAL_RESTRICTION", "containing the same vertices"
    ):
        return "Why should we require that the Hamiltonian cycle and Hamiltonian path contain the same vertices?"
    if submission.does_path_exist(
        "ADDITIONAL_RESTRICTION", "containing the same edges"
    ):
        return "Why should we require that the Hamiltonian cycle and Hamiltonian path contain the same edges?"
    return None


def generate(data: QuestionData) -> None:
    data["params"]["iff_claim_cfg"] = get_ham_path_cycle_cfg().to_json_string()


def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(
        sw_gu.GraphStudentSubmission, get_ham_path_cycle_cfg()
    )

    grader.add_constraint(sw_gu.used_both_graphs, 0.025)
    grader.add_constraint(sw_gu.used_iff_structure, 0.05)
    grader.add_constraint(sw_gu.correct_object({"Hamiltonian cycle"}), 0.2)
    grader.add_constraint(
        sw_gu.correct_object({"Hamiltonian path"}, isGprime=True), 0.4
    )
    grader.add_constraint(avoid_additional_restrictions)

    grader.grade_question(data, "iff_claim")
    pl.set_weighted_score_data(data)
