import prairielearn as pl
import theorielearn.scaffolded_writing.dp_utils as sw_du
from theorielearn.scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from theorielearn.scaffolded_writing.dp_cfgs import get_partition_sum_cfg
from theorielearn.shared_utils import QuestionData


def array_reduces_handler(submission: sw_du.DPStudentSubmission) -> str:
    return "if we decide to place a plus sign after the first digit, then we would need to compute the minimum sum that can be obtained from A[2..n]"


def term_length_reduces_handler(submission: sw_du.DPStudentSubmission) -> str:
    if submission.does_path_exist("PREFIX_SUBPROBLEM"):
        first_or_last = "last"
        second_or_second_last = "second-to-last"
    else:
        first_or_last = "first"
        second_or_second_last = "second"

    return f"if we decide to group the {first_or_last} two digits into a 2-digit term, then we would need to enforce that the {second_or_second_last} term of the summation is 1 <em>or</em> 3 digits long"


def term_position_reduces_handler(submission: sw_du.DPStudentSubmission) -> str:
    if submission.does_path_exist("PREFIX_SUBPROBLEM"):
        first_or_last = "last"
        restricted_index = "A[n-3]"
    else:
        first_or_last = "first"
        restricted_index = "A[4]"

    return f"if we decide to group the {first_or_last} three digits into a 3-digit term, then we would need to restrict the length of the term that {restricted_index} belongs to"


def generate(data: QuestionData) -> None:
    data["params"]["subproblem_definition_cfg"] = (
        get_partition_sum_cfg().to_json_string()
    )


def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_partition_sum_cfg()
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
        sw_du.reduces_recursively_constraint("SUBARRAY", array_reduces_handler), 0.4
    )
    grader.add_constraint(
        sw_du.reduces_recursively_constraint(
            "RESTRICTED_TERM_INDEX", term_position_reduces_handler
        ),
        0.5,
    )
    grader.add_constraint(
        sw_du.reduces_recursively_constraint(
            "TERM_LENGTH", term_length_reduces_handler
        ),
        0.6,
    )
    grader.add_constraint(
        sw_du.no_irrelevant_restrictions_constraint("NUM_TWO_DIGIT_TERMS_RESTRICTION"),
        0.7,
    )
    grader.add_constraint(sw_du.no_double_ended_parameterization_constraint())

    grader.grade_question(data, "subproblem_definition")
    pl.set_weighted_score_data(data)
