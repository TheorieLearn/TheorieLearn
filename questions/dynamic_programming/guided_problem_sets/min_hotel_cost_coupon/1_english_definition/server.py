import prairielearn as pl
import theorielearn.scaffolded_writing.dp_utils as sw_du
from theorielearn.scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from theorielearn.scaffolded_writing.dp_cfgs import get_hotel_cost_coupons_cfg
from theorielearn.shared_utils import QuestionData


def array_reduces_handler(submission: sw_du.DPStudentSubmission) -> str:
    return "after Momo travels through the first hotel, we would need to compute the maximum sum that can be obtained from mile 2 to mile n"


def num_two_digit_handler(submission: sw_du.DPStudentSubmission) -> str:
    first_or_last = (
        "last" if submission.does_path_exist("PREFIX_SUBPROBLEM") else "first"
    )

    return f"if Momo uses a coupon on the {first_or_last} hotel, then we would need to enforce that the rest of the trip uses at most <em>(k-1)</em> coupons"


def generate(data: QuestionData) -> None:
    data["params"]["subproblem_definition_cfg"] = (
        get_hotel_cost_coupons_cfg().to_json_string()
    )


def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_hotel_cost_coupons_cfg()
    )

    grader.add_constraint(sw_du.declare_func_constraint(), 0.05)
    grader.add_constraint(sw_du.correct_noun_and_adj_constraint("cost", "minimum"), 0.1)
    grader.add_constraint(sw_du.descriptive_func_name_constraint("MinCost"), 0.15)
    grader.add_constraint(
        sw_du.explain_params_constraint(variables_in_problem={"n", "k", "s"}), 0.25
    )
    grader.add_constraint(
        sw_du.decoupled_parameters_constraint(
            SUBARRAY="a hotel",
            COMPARISON_RHS="the number of coupons",
            HOTEL_STATUS="whether Momo stayed in a hotel",
        ),
        0.3,
    )

    grader.add_constraint(
        sw_du.can_compute_final_answer_constraint(
            "NUM_COUPONS_RESTRICTION",
            "COMPARISON_OPERATOR",
            "VIABLE_COMPARISON_OPERATOR",
            feedback_elaboration="at most k coupons are used",
        ),
        0.4,
    )

    grader.add_constraint(
        sw_du.can_compute_final_answer_constraint(
            "VIABLE_HOTEL_STATUS",
            feedback_elaboration="Momo stays in at least one hotel every two miles",
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

    grader.add_constraint(sw_du.no_double_ended_parameterization_constraint())

    grader.grade_question(data, "subproblem_definition")
    pl.set_weighted_score_data(data)
