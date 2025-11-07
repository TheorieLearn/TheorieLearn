import prairielearn as pl
import theorielearn.scaffolded_writing.dp_utils as sw_du
from theorielearn.scaffolded_writing.constraint_based_grader import (
    IncrementalConstraintGrader,
)
from theorielearn.scaffolded_writing.dp_cfgs import get_grasslearn_2var_cfg
from theorielearn.shared_utils import QuestionData


def array_reduces_handler(submission: sw_du.DPStudentSubmission) -> str:
    return "if we decide to answer the first question incorrectly, then we would need to compute the minimum number of minutes required to earn at least p points from Questions 2 through n"


def num_points_reduces_handler(submission: sw_du.DPStudentSubmission) -> str:
    return "if we decide to answer the first question correctly, then we would need to enforce that we earn at least <b><em>(p-1)</em></b> points from the rest of the questions"


def generate(data: QuestionData) -> None:
    data["params"]["subproblem_definition_cfg"] = get_grasslearn_2var_cfg().to_json_string()


def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_grasslearn_2var_cfg()
    )

    grader.add_constraint(sw_du.declare_func_constraint(), 0.05)
    grader.add_constraint(
        sw_du.correct_noun_and_adj_constraint(
            correct_noun="number of minutes",
            correct_adj="minimum",
        ),
        0.1,
    )
    grader.add_constraint(
        sw_du.descriptive_func_name_constraint(correct_func_name="MinMinutes"),
        0.15,
    )
    grader.add_constraint(
        sw_du.explain_params_constraint(variables_in_problem={"n", "p"}), 0.25
    )
    grader.add_constraint(
        sw_du.decoupled_parameters_constraint(
            SUBARRAY="the index of a question",
            NUM_POINTS="the number of points required",
        ),
        0.3,
    )
    grader.add_constraint(
        sw_du.can_compute_final_answer_constraint(
            "NUM_POINTS_RESTRICTION",
            "COMPARISON_OPERATOR",
            "VIABLE_COMPARISON_OPERATOR",
            feedback_elaboration="you earn at least p points",
        ),
        0.4,
    )
    grader.add_constraint(
        sw_du.reduces_recursively_constraint(
            field_requiring_parameters="SUBARRAY",
            get_unhandled_scenario=array_reduces_handler,
        ),
        0.5,
    )
    grader.add_constraint(
        sw_du.reduces_recursively_constraint(
            field_requiring_parameters="NUM_POINTS",
            get_unhandled_scenario=num_points_reduces_handler,
        ),
        0.7,
    )

    grader.add_constraint(sw_du.no_double_ended_parameterization_constraint())

    grader.grade_question(data, "subproblem_definition")
    pl.set_weighted_score_data(data)
