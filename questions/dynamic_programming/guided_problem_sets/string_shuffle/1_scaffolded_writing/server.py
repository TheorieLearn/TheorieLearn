import prairielearn as pl
import theorielearn.scaffolded_writing.dp_utils as sw_du
from theorielearn.scaffolded_writing.constraint_based_grader import (
    IncrementalConstraintGrader,
)
from theorielearn.scaffolded_writing.dp_cfgs import get_valid_shuffle_cfg
from theorielearn.shared_utils import QuestionData


# This constraint is used to check that the student returns True when conditions are met.
def initial_true_constraint() -> sw_du.ConstraintT:
    def constraint(submission: sw_du.DPStudentSubmission) -> str | None:
        if submission.does_path_exist("FUNCTION_OUTPUT", "BOOL", "True"):
            return None
        return "Our function should output True when the conditions for a valid shuffle are met."

    return constraint


# This constraint checks whether the student defines the subarray of C as either C[1..i+j] or C[1..k].
def correct_C_definition_constraint() -> sw_du.ConstraintT:
    def constraint(submission: sw_du.DPStudentSubmission) -> str | None:
        if submission.does_path_exist("C[1..k]") or submission.does_path_exist(
            "C[1..i+j]"
        ):
            return None
        if submission.does_path_exist("C"):
            return "You should talk about a prefix of C, not the whole string."
        if (
            submission.does_path_exist("C[i]")
            or submission.does_path_exist("C[j]")
            or submission.does_path_exist("C[k]")
        ):
            return "You should talk about a prefix of C, not a single character."
        return "Does this parameter make sense to use within C?"

    return constraint


# This constraint checks whether the student defines the subarray of A as either A[1..i] or A[1..j].
def correct_A_definition_constraint() -> sw_du.ConstraintT:
    def constraint(submission: sw_du.DPStudentSubmission) -> str | None:
        if submission.does_path_exist("A[1..i]") or submission.does_path_exist(
            "A[1..j]"
        ):
            return None
        if submission.does_path_exist("A"):
            return "You should talk about a prefix of A, not the whole string."
        if submission.does_path_exist("A[i]") or submission.does_path_exist("A[j]"):
            return "You should talk about a prefix of A, not a single character."
        return "Does this parameter make sense to use within A?"

    return constraint


# This constraint checks whether the student defines the subarray of B as either B[1..i] or B[1..j],
# making sure not to use the same parameter twice.
def correct_B_definition_constraint() -> sw_du.ConstraintT:
    def constraint(submission: sw_du.DPStudentSubmission) -> str | None:
        if (
            submission.does_path_exist("A[1..i]")
            and submission.does_path_exist("B[1..j]")
        ) or (
            submission.does_path_exist("B[1..i]")
            and submission.does_path_exist("A[1..j]")
        ):
            return None
        if submission.does_path_exist("B"):
            return "You should talk about a prefix of B, not the whole string."
        if submission.does_path_exist("B[i]") or submission.does_path_exist("B[j]"):
            return "You should talk about a prefix of B, not a single character."
        return "Does this parameter make sense to use within B?"

    return constraint


# This constraint checks whether the student defines what happens when the condition is *not* met.
def false_case_constraint() -> sw_du.ConstraintT:
    def constraint(submission: sw_du.DPStudentSubmission) -> str | None:
        if submission.does_path_exist("FALSE_CASE", "BOOL", "False"):
            return None
        if submission.does_path_exist("FALSE_CASE", "BOOL", "True"):
            return "Our function should output False when the conditions for a valid shuffle are not met."
        return "What happens when the conditions for a valid shuffle are not met?"

    return constraint


# The student can define a valid subproblem as ValidShuffle(i,j,k) or ValidShuffle(i,j). This constraint
# checks whether the student has defined the latter, as the former has a redundant parameter.
def k_clause_constraint() -> sw_du.ConstraintT:
    def constraint(submission: sw_du.DPStudentSubmission) -> str | None:
        if submission.does_path_exist("ValidShuffle(i,j,k)"):
            return "This recursive definition is correct, but can be improved.  Notice that in every recursive subproblem, the parameter k is  equal to i+j. This observation allows us to remove a parameter from the function, which leads to faster algorithm."
        return None

    return constraint


def generate(data: QuestionData) -> None:
    data["params"]["subproblem_definition_cfg"] = (
        get_valid_shuffle_cfg().to_json_string()
    )


def grade(data: QuestionData) -> None:
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_valid_shuffle_cfg()
    )
    grader.add_constraint(sw_du.declare_func_constraint(), 0.05)
    grader.add_constraint(initial_true_constraint(), 0.1)
    grader.add_constraint(sw_du.descriptive_func_name_constraint("ValidShuffle"), 0.15)
    grader.add_constraint(sw_du.explain_params_constraint(set()), 0.25)
    grader.add_constraint(correct_C_definition_constraint(), 0.40)
    grader.add_constraint(correct_A_definition_constraint(), 0.50)
    grader.add_constraint(correct_B_definition_constraint(), 0.70)
    grader.add_constraint(false_case_constraint(), 0.85)
    grader.add_constraint(k_clause_constraint(), 1)
    grader.grade_question(data, "subproblem_definition")
    pl.set_weighted_score_data(data)
