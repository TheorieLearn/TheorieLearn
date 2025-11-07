from typing import Any, Dict, List, Optional, Tuple

import prairielearn as pl
from theorielearn.scaffolded_writing.cfg import ScaffoldedWritingCFG
from theorielearn.scaffolded_writing.student_submission import StudentSubmission
from theorielearn.shared_utils import grade_question_parameterized

cfg = ScaffoldedWritingCFG.fromstring("""
    START -> STATEMENT_ABOUT_0 \
           | STATEMENT_ABOUT_1 \
           | STATEMENT_ABOUT_0 STATEMENT_ABOUT_1 \
           | STATEMENT_ABOUT_1 STATEMENT_ABOUT_0

    STATEMENT_ABOUT_0 -> "blocks of 0s" RESTRICTION "." \
                       | "blocks of 0s" RESTRICTION "," "except for" "blocks of 0s" EXCEPTION_CLAUSE "."

    STATEMENT_ABOUT_1 -> "blocks of 1s" RESTRICTION "." \
                       | "blocks of 1s" RESTRICTION "," "except for" "blocks of 1s" EXCEPTION_CLAUSE "."

    RESTRICTION -> "must have length" LENGTH_REQUIREMENT | "can have any length"

    LENGTH_REQUIREMENT -> "exactly 1" \
                        | "at least 2" | "at most 2" | "exactly 2" \
                        | "at least 3" | "at most 3" | "exactly 3" \

    EXCEPTION_CLAUSE -> "that appear at the" EXCEPTION_POSITION "of the string" "," "which" RESTRICTION \
                      | "that appear at the" EXCEPTION_POSITION "of the string"

    EXCEPTION_POSITION -> "start" | "end" | "start or end"
""")

# "at most 1" an option because it means the same thing as "exactly 1"
# "at least 1" isn't an option because it's the same as not having any restriction at all
# all other numbers can have any comparison operator (at least, at most, or exactly) applied to them


def generate(data: pl.QuestionData) -> None:
    data["params"]["statement_cfg"] = cfg.to_json_string()


def grade_statement(tokens: List[str]) -> Tuple[bool, Optional[str]]:
    submission = StudentSubmission(tokens, cfg)

    if submission.does_path_exist(
        "STATEMENT_ABOUT_0", "RESTRICTION", "LENGTH_REQUIREMENT"
    ) or submission.does_path_exist(
        "STATEMENT_ABOUT_0", "EXCEPTION_CLAUSE", "RESTRICTION", "LENGTH_REQUIREMENT"
    ):
        return (
            False,
            "Are you sure there should be any length restrictions on the blocks of 0s?",
        )

    if not submission.does_path_exist(
        "STATEMENT_ABOUT_1"
    ) or submission.does_path_exist(
        "STATEMENT_ABOUT_1", "RESTRICTION", "can have any length"
    ):
        return (
            False,
            "Are there any length restrictions on blocks of 1s in the middle of the string?",
        )

    if (
        submission.does_path_exist(
            "STATEMENT_ABOUT_1", "RESTRICTION", "LENGTH_REQUIREMENT", "exactly 1"
        )
        or submission.does_path_exist(
            "STATEMENT_ABOUT_1", "RESTRICTION", "LENGTH_REQUIREMENT", "at most 2"
        )
        or submission.does_path_exist(
            "STATEMENT_ABOUT_1", "RESTRICTION", "LENGTH_REQUIREMENT", "at most 3"
        )
    ):
        return (
            False,
            "Should blocks of 1s with length 1 be allowed in the middle of the string?",
        )

    if submission.does_path_exist(
        "STATEMENT_ABOUT_1", "RESTRICTION", "LENGTH_REQUIREMENT", "at least 3"
    ) or submission.does_path_exist(
        "STATEMENT_ABOUT_1", "RESTRICTION", "LENGTH_REQUIREMENT", "exactly 3"
    ):
        return (
            False,
            "A block of 1s with length 2 should be allowed, right? For example, consider 0110.",
        )

    if submission.does_path_exist(
        "STATEMENT_ABOUT_1", "RESTRICTION", "LENGTH_REQUIREMENT", "exactly 2"
    ):
        return (
            False,
            "A block of 1s with length 3 should be allowed, right? For example, consider 01110.",
        )

    if not submission.does_path_exist("STATEMENT_ABOUT_1", "EXCEPTION_CLAUSE"):
        return False, "Are there any exceptions to the restriction on blocks of 1s?"

    if submission.does_path_exist(
        "STATEMENT_ABOUT_1", "EXCEPTION_CLAUSE", "EXCEPTION_POSITION", "start"
    ):
        return (
            False,
            "Does the exception also apply to blocks of 1s at the end of the string?",
        )

    if submission.does_path_exist(
        "STATEMENT_ABOUT_1", "EXCEPTION_CLAUSE", "EXCEPTION_POSITION", "end"
    ):
        return (
            False,
            "Does the exception also apply to blocks of 1s at the start of the string?",
        )

    if submission.does_path_exist(
        "STATEMENT_ABOUT_1", "EXCEPTION_CLAUSE", "RESTRICTION", "LENGTH_REQUIREMENT"
    ):
        return (
            False,
            "Should there be any length requirements on blocks of 1s at the start/end of the string?",
        )

    return True, None


def grade(data: pl.QuestionData) -> None:
    grade_question_parameterized(data, "statement", grade_statement)
    pl.set_weighted_score_data(data)
