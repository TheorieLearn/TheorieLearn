import prairielearn as pl
import theorielearn.scaffolded_writing.dp_utils as sw_du
from theorielearn.scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from theorielearn.scaffolded_writing.dp_cfgs import get_partition_sum_cfg
from theorielearn.shared_utils import QuestionData


def array_reduces_handler(submission: sw_du.DPStudentSubmission) -> str:
    return "if we decide to place a plus sign after the first digit, then we would need to compute the maximum sum that can be obtained from A[2..n]"


def num_two_digit_handler(submission: sw_du.DPStudentSubmission) -> str:
    first_or_last = (
        "last" if submission.does_path_exist("PREFIX_SUBPROBLEM") else "first"
    )

    return f"if we decide to group the {first_or_last} two digits into a 2-digit term, then we would need to enforce that the rest of the summation uses at most <b><em>(t-1)</em></b> 2-digit terms"


def generate(data: QuestionData) -> None:
    data["params"]["subproblem_definition_cfg"] = (
        get_partition_sum_cfg().to_json_string()
    )


def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_partition_sum_cfg()
    )

    grader.add_constraint(sw_du.declare_func_constraint(), 0.05)
    grader.add_constraint(sw_du.correct_noun_and_adj_constraint("sum", "maximum"), 0.1)
    grader.add_constraint(sw_du.descriptive_func_name_constraint("MaxSum"), 0.15)
    grader.add_constraint(
        sw_du.explain_params_constraint(variables_in_problem={"n", "t"}), 0.25
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
        sw_du.can_compute_final_answer_constraint(
            "NUM_TWO_DIGIT_TERMS_RESTRICTION",
            "COMPARISON_OPERATOR",
            "VIABLE_COMPARISON_OPERATOR",
            feedback_elaboration="at most t 2-digit terms are used",
        ),
        0.4,
    )
    grader.add_constraint(
        sw_du.reduces_recursively_constraint("SUBARRAY", array_reduces_handler), 0.5
    )
    grader.add_constraint(
        sw_du.reduces_recursively_constraint("COMPARISON_RHS", num_two_digit_handler),
        0.6,
    )
    grader.add_constraint(
        sw_du.no_irrelevant_restrictions_constraint("FIRST_OR_LAST_TERM_RESTRICTION"),
        0.7,
    )
    grader.add_constraint(sw_du.no_double_ended_parameterization_constraint())

    grader.grade_question(data, "subproblem_definition")
    pl.set_weighted_score_data(data)
