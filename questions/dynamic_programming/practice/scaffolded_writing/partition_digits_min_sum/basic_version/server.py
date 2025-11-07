import prairielearn as pl
import theorielearn.scaffolded_writing.dp_utils as sw_du
from theorielearn.scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from theorielearn.scaffolded_writing.dp_cfgs import get_partition_min_sum_cfg
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["subproblem_definition_cfg"] = (
        get_partition_min_sum_cfg().to_json_string()
    )

def array_reduces_handler(submission: sw_du.DPStudentSubmission) -> str:
    return "if we decide to place a plus sign after the first digit, then we would need to compute the minimum sum that can be obtained from A[2..n] using at most j 1-digit terms"

def one_digit_term_handler(submission: sw_du.DPStudentSubmission) -> str:
    return "if we decide to use a 1-digit term, then we would need to compute the minimum sum that can be obtained from A[2..n] without using any more 1-digit terms"



def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_partition_min_sum_cfg()
    )

    grader.add_constraint(sw_du.declare_func_constraint(), 0.05)
    grader.add_constraint(sw_du.correct_noun_and_adj_constraint("sum", "minimum"), 0.1)
    grader.add_constraint(sw_du.descriptive_func_name_constraint("MinSum"), 0.15)
    grader.add_constraint(
        sw_du.explain_params_constraint(variables_in_problem={"n"}), 0.25
    )
    grader.add_constraint(
        sw_du.decoupled_parameters_constraint(
            SUBARRAY="an array index",
            COMPARISON_RHS="the number of 2-digit terms",
            TERM_LENGTH="a term length",
        ),
        0.3,
    )

    grader.add_constraint(
        sw_du.reduces_recursively_constraint("COMPARISON_RHS", one_digit_term_handler),
        0.4,
    )
    grader.add_constraint(
        sw_du.reduces_recursively_constraint("SUBARRAY", array_reduces_handler), 0.6
    )

    grader.add_constraint(sw_du.no_double_ended_parameterization_constraint())

    grader.grade_question(data, "subproblem_definition")
    pl.set_weighted_score_data(data)
