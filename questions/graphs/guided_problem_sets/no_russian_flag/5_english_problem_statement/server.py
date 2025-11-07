from typing import Optional

import prairielearn as pl
import theorielearn.scaffolded_writing.scaffolded_graph_utils as sw_gu
from theorielearn.scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from theorielearn.scaffolded_writing.graph_cfgs import get_no_russian_flag_cfg
from theorielearn.shared_utils import QuestionData


def defined_G_is_russian(submission: sw_gu.GraphStudentSubmission) -> Optional[str]:
    if not submission.does_path_exist(
        "STATEMENT_ABOUT_G", "OBJECT", "RUSSIAN", "with no Russian flags"
    ):
        return "Do we care about these generic walks within G?"
    return None


def defined_Gprime_is_not_russian(
    submission: sw_gu.GraphStudentSubmission,
) -> Optional[str]:
    if submission.does_path_exist(
        "STATEMENT_ABOUT_G_PRIME", "OBJECT", "RUSSIAN", "with no Russian flags"
    ):
        return "Does G' have colors on its edges to talk about Russian flag walks?"
    return None


def defined_general_value(submission: sw_gu.GraphStudentSubmission) -> Optional[str]:
    if submission.does_path_exist("T_GENERAL", "(t, q) for all q in {None, W, WB}"):
        return "Do we need all three paths?"
    return None


def generate(data: QuestionData) -> None:
    data["params"]["no_russian_flag_cfg"] = get_no_russian_flag_cfg().to_json_string()


def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(
        sw_gu.GraphStudentSubmission, get_no_russian_flag_cfg()
    )

    grader.add_constraint(sw_gu.used_both_graphs, 0.025)
    grader.add_constraint(sw_gu.used_iff_structure, 0.05)
    grader.add_constraint(sw_gu.correct_object({"walk"}), 0.1)
    grader.add_constraint(defined_G_is_russian, 0.15)
    grader.add_constraint(sw_gu.defined_starting_location("walk"), 0.2)
    grader.add_constraint(
        sw_gu.defined_simple_terminal_node(
            "s",
            feedback="G does not have ordered pairs for \
                                                             nodes.",
        ),
        0.3,
    )
    grader.add_constraint(
        sw_gu.defined_simple_terminal_node(
            "t",
            isEnd=True,
            feedback="G does not have ordered \
                                                             pairs for nodes.",
        ),
        0.4,
    )
    grader.add_constraint(sw_gu.correct_object({"walk", "path"}, isGprime=True), 0.6)
    grader.add_constraint(defined_Gprime_is_not_russian, 0.65)
    grader.add_constraint(sw_gu.defined_starting_location("walk", isGprime=True), 0.7)
    grader.add_constraint(
        sw_gu.defined_simple_terminal_node(
            "(s, None)",
            isEnd=False,
            isGprime=True,
            feedback="G' \
                                                             has ordered pairs for nodes; make sure to select the \
                                                             appropriate terminal vertices.",
        ),
        0.8,
    )
    grader.add_constraint(
        sw_gu.defined_general_terminal_node(isEnd=True, isGprime=True), 0.9
    )
    grader.add_constraint(defined_general_value)

    grader.grade_question(data, "no_russian_flag")
    pl.set_weighted_score_data(data)
