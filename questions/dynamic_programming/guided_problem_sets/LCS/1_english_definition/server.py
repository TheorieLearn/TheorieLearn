import prairielearn as pl
import theorielearn.scaffolded_writing.dp_utils as sw_du
from theorielearn.scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from theorielearn.scaffolded_writing.dp_cfgs import get_lcs_cfg
from theorielearn.shared_utils import QuestionData


# Restricts usage of A[1..n] or B[1..m], which doesn't reduce
def array_reduces_handler_A(submission: sw_du.DPStudentSubmission) -> str:
    return "after we decide to not use A[1] in our subsequence, we would next need to consider A[2..n]"


def array_reduces_handler_B(submission: sw_du.DPStudentSubmission) -> str:
    return "after we decide to not use B[1] in our subsequence, we would next need to consider B[2..m]"


# Restricts usage of non-descriptive output nouns
def correct_noun_constraint(correct_noun: str) -> sw_du.ConstraintT:
    def constraint(submission: sw_du.DPStudentSubmission) -> str | None:
        is_noun_correct = submission.does_path_exist("OUTPUT_NOUN", correct_noun)

        if is_noun_correct:
            return None

        if submission.does_path_exist("OUTPUT_NOUN", "answer"):
            return (
                'Please be more precise about what quantity the function actually outputs. \
                Just saying "answer" is too vague.'
            )

        return (
            "It seems like the quantity outputted by your function is not directly relevant \
            for solving the original problem."
        )

    return constraint


# Restricts usage of double-ended subproblems. Potentially unused?
def no_double_ended_parameterization_constraint() -> sw_du.ConstraintT:
    def constraint(submission: sw_du.DPStudentSubmission) -> str | None:
        if not submission.does_path_exist(
            "DOUBLE_ENDED_A"
        ) and not submission.does_path_exist("DOUBLE_ENDED_B"):
            return None

        return (
            "You parametrized both the start and end index of your subproblem, but for this \
            problem, your subproblem doesn't need to reduce on both sides. Each possible choice \
                should only cause your subproblem to get smaller on one side. Your subproblem \
                    definition might still be viable, but this slows down your algorithm by a factor \
                        of $O(n)$. (Some other problems actually do require reducing on both sides, e.g. \
                            see the Longest Palindromic Subsequence problem from lab.)"
        )

    return constraint


# Restricts usage of inconsistent eval order of the two strings
def consistent_evaluation_order_constraint() -> sw_du.ConstraintT:
    def constraint(submission: sw_du.DPStudentSubmission) -> str | None:
        eval_order_A = (
            "prefix"
            if submission.does_path_exist("VALID_DEFA", "A[1..i]")
            or submission.does_path_exist("VALID_DEFA", "A[1..j]")
            else "suffix"
        )
        eval_order_B = (
            "prefix"
            if submission.does_path_exist("VALID_DEFB", "B[1..i]")
            or submission.does_path_exist("VALID_DEFB", "B[1..j]")
            else "suffix"
        )

        if eval_order_A == eval_order_B:
            return None

        return f"You're evaluating A from a {eval_order_A} order, yet B from a {eval_order_B} order. \
            However, we need to build up a common subsequence from either the start or the end, so the \
                evaluation order of the two strings should be consistent."

    return constraint


def generate(data: QuestionData) -> None:
    data["params"]["subproblem_definition_cfg"] = get_lcs_cfg().to_json_string()


def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(sw_du.DPStudentSubmission, get_lcs_cfg())

    grader.add_constraint(sw_du.declare_func_constraint(), 0.05)
    grader.add_constraint(
        correct_noun_constraint("length of the longest common subsequence"), 0.1
    )
    grader.add_constraint(sw_du.descriptive_func_name_constraint("LCS"), 0.15)
    grader.add_constraint(
        sw_du.explain_params_constraint(variables_in_problem={"n", "m"}), 0.25
    )
    grader.add_constraint(
        sw_du.decoupled_parameters_constraint(
            DEFA="index of string A", DEFB="index of string B"
        ),
        0.3,
    )
    grader.add_constraint(
        sw_du.reduces_recursively_constraint("DEFA", array_reduces_handler_A), 0.6
    )
    grader.add_constraint(
        sw_du.reduces_recursively_constraint("DEFB", array_reduces_handler_B), 0.6
    )
    grader.add_constraint(no_double_ended_parameterization_constraint(), 0.7)
    grader.add_constraint(consistent_evaluation_order_constraint())

    grader.grade_question(data, "subproblem_definition")
    pl.set_weighted_score_data(data)
