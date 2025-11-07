from typing import List

import pytest
import theorielearn.scaffolded_writing.dp_utils as sw_du
from theorielearn.scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from theorielearn.scaffolded_writing.dp_cfgs import get_partition_sum_cfg
from theorielearn.shared_utils import QuestionData, get_partial_score


def verify_incremental_constraint_grader_exception_submission_type() -> None:
    class testClass:
        variable = 1

    # Check that grader must be given a valid student submission type
    with pytest.raises(TypeError, match="is not a subclass of StudentSubmission"):
        grader = IncrementalConstraintGrader(testClass, get_partition_sum_cfg())  # type: ignore

        grader.add_constraint(sw_du.declare_func_constraint(), 0)


def verify_incremental_constraint_grader_exception_credit_range() -> None:
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_partition_sum_cfg()
    )

    # Check that partial credit must be in the range (0, 1]
    with pytest.raises(ValueError, match=r"partial credit is not in \(0,1]"):
        grader.add_constraint(sw_du.declare_func_constraint(), -1)

    with pytest.raises(ValueError, match=r"partial credit is not in \(0,1]"):
        grader.add_constraint(sw_du.declare_func_constraint(), 0)

    with pytest.raises(ValueError, match=r"partial credit is not in \(0,1]"):
        grader.add_constraint(sw_du.declare_func_constraint(), 2)


def verify_incremental_constraint_grader_exception_constraint_order() -> None:
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_partition_sum_cfg()
    )

    grader.add_constraint(sw_du.declare_func_constraint(), 0.5)

    # Check that partial scores must be increasing for this grader type
    with pytest.raises(ValueError, match="value not increasing"):
        grader.add_constraint(sw_du.declare_func_constraint(), 0.3)

    grader.add_constraint(sw_du.declare_func_constraint(), 0.5)

    # Check that partial scores must be increasing after an update
    with pytest.raises(ValueError, match="value not increasing"):
        grader.add_constraint(sw_du.declare_func_constraint(), 0.3)


def verify_incremental_constraint_grader_exception_partial_scores(
    question_data: QuestionData,
) -> None:
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_partition_sum_cfg()
    )

    # Check that grader is called with a nonzero number of constraints
    with pytest.raises(ValueError, match="No constraints set"):
        grader.grade_question(question_data, "name")

    grader.add_constraint(sw_du.declare_func_constraint(), 0.5)

    # Check that last partial score given to grader grants full credit
    with pytest.raises(ValueError, match="doesn't grant full credit"):
        grader.grade_question(question_data, "name")


@pytest.mark.parametrize(
    "student_tokens, expected_grade",
    [
        (
            [
                "define",
                "the subproblem",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                ".",
            ],
            0.0,
        ),
        (["define", "DP(i)", "to be the", "answer", "that can be obtained", "."], 0.05),
        (
            [
                "define",
                "DP(i)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                ".",
            ],
            0.1,
        ),
        (
            [
                "define",
                "MaxSum(i)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                ".",
            ],
            0.15,
        ),
        (
            [
                "define",
                "MaxSum(i)",
                "to be the",
                "maximum",
                "sum",
                "that can be obtained",
                "from",
                "A[i..n]",
                "using",
                "at most",
                "t",
                "2-digit terms",
                ".",
            ],
            1.0,
        ),
    ],
)
def verify_incremental_constraint_grader(
    student_tokens: List[str], expected_grade: float, question_data: QuestionData
) -> None:
    # Configure grader
    grader = IncrementalConstraintGrader(
        sw_du.DPStudentSubmission, get_partition_sum_cfg()
    )

    grader.add_constraint(sw_du.declare_func_constraint(), 0.05)
    grader.add_constraint(sw_du.correct_noun_and_adj_constraint("sum", "maximum"), 0.1)
    grader.add_constraint(sw_du.descriptive_func_name_constraint("MaxSum"), 0.15)
    grader.add_constraint(
        sw_du.explain_params_constraint(variables_in_problem={"n", "t"})
    )

    # Set up data dictionary
    question_name = "name"

    question_data["submitted_answers"] = {question_name: student_tokens}

    # Grade question
    grader.grade_question(question_data, question_name)
    assert get_partial_score(question_data, question_name) == expected_grade

    # Assert we get feedback if we didn't get full credit
    if expected_grade < 1.0:
        assert question_data["feedback"][question_name]
