from typing import Optional

import prairielearn as pl
import theorielearn.scaffolded_writing.scaffolded_graph_utils as sw_gu
from theorielearn.scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from theorielearn.scaffolded_writing.graph_cfgs import get_french_flag_cfg
from theorielearn.shared_utils import QuestionData


def defined_general_value(submission: sw_gu.GraphStudentSubmission) -> Optional[str]:
    if not submission.does_path_exist("I_CHARACTERISTIC", "NUMBER_CHARACTERISTIC"):
        return "Shouldn't i be more general than this?"
    return None


def defined_number_characteristic(
    submission: sw_gu.GraphStudentSubmission,
) -> Optional[str]:
    if not submission.does_path_exist(
        "I_CHARACTERISTIC", "NUMBER_CHARACTERISTIC", "between 0 and 2"
    ):
        return "Did you specify the right bounds for i?"
    return None


def generate(data: QuestionData) -> None:
    data["params"]["french_flag_cfg"] = get_french_flag_cfg().to_json_string()


def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(
        sw_gu.GraphStudentSubmission, get_french_flag_cfg()
    )

    grader.add_constraint(sw_gu.used_both_graphs, 0.025)
    grader.add_constraint(sw_gu.used_iff_structure, 0.05)
    grader.add_constraint(sw_gu.correct_object({"french flag walk"}), 0.1)
    grader.add_constraint(sw_gu.defined_starting_location("french flag walk"), 0.2)
    grader.add_constraint(
        sw_gu.defined_simple_terminal_node(
            "s", feedback="G does not have ordered pairs for nodes"
        ),
        0.3,
    )
    grader.add_constraint(
        sw_gu.defined_simple_terminal_node(
            "t", isEnd=True, feedback="G does not have ordered pairs for nodes"
        ),
        0.4,
    )
    grader.add_constraint(sw_gu.correct_object({"walk", "path"}, isGprime=True), 0.6)
    grader.add_constraint(sw_gu.defined_starting_location("walk", isGprime=True), 0.7)
    grader.add_constraint(
        sw_gu.defined_simple_terminal_node(
            "(s, 0)",
            isEnd=False,
            isGprime=True,
            feedback="G' has ordered pairs for nodes",
        ),
        0.8,
    )
    grader.add_constraint(
        sw_gu.defined_general_terminal_node(isEnd=True, isGprime=True), 0.85
    )
    grader.add_constraint(defined_general_value, 0.9)
    grader.add_constraint(defined_number_characteristic)

    grader.grade_question(data, "french_flag")
    pl.set_weighted_score_data(data)
