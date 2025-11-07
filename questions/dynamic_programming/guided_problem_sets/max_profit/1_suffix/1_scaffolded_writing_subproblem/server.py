from typing import Optional

import prairielearn as pl
import theorielearn.scaffolded_writing.dp_utils as sw_du
from theorielearn.scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from theorielearn.scaffolded_writing.dp_cfgs import get_max_profit_cfg
from theorielearn.shared_utils import QuestionData


def array_reduces_handler(submission: sw_du.DPStudentSubmission) -> str:
    return "if we decide to take the first trial and skip[0] = 3, then we would need to compute the maximum profit that can be obtained from Trials 5 through n"


def no_prefex_subproblems_constraint() -> sw_du.ConstraintT:
    def constraint(submission: sw_du.DPStudentSubmission) -> Optional[str]:
        if not submission.does_path_exist("PREFIX_SUBPROBLEM"):
            return None
        return "Using prefix subproblems actually doesn't work for this problem, because these prefix subproblems don't reduce recursively. Think about why this is the case and why suffix subproblems don't have the same issue."

    return constraint


def generate(data: QuestionData) -> None:
    data["params"]["subproblem_definition_cfg"] = get_max_profit_cfg().to_json_string()


def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_max_profit_cfg()
    )

    grader.add_constraint(sw_du.declare_func_constraint(), 0.05)
    grader.add_constraint(
        sw_du.correct_noun_and_adj_constraint("profit", "maximum"), 0.1
    )
    grader.add_constraint(sw_du.descriptive_func_name_constraint("MaxProfit"), 0.15)
    grader.add_constraint(
        sw_du.explain_params_constraint(variables_in_problem={"n"}), 0.25
    )
    grader.add_constraint(
        sw_du.decoupled_parameters_constraint(
            SUBARRAY="the index of a trial",
            COMPARISON_RHS="the number of trials accepted",
        ),
        0.3,
    )
    grader.add_constraint(
        sw_du.reduces_recursively_constraint("SUBARRAY", array_reduces_handler), 0.5
    )
    grader.add_constraint(no_prefex_subproblems_constraint(), 0.6)
    grader.add_constraint(
        sw_du.no_irrelevant_restrictions_constraint("NUM_TRIALS_RESTRICTION"), 0.7
    )
    grader.add_constraint(sw_du.no_double_ended_parameterization_constraint())

    grader.grade_question(data, "subproblem_definition")
    pl.set_weighted_score_data(data)
