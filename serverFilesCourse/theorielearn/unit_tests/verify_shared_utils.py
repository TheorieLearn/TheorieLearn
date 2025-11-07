from __future__ import annotations

from typing import Any, Optional

import pytest
import theorielearn.shared_utils as su

@pytest.fixture
def qdata() -> su.QuestionData:
    """
    Prepare data dict
    """
    data: su.QuestionData = {
        "params": dict(),
        "correct_answers": dict(),
        "submitted_answers": dict(),
        "format_errors": dict(),
        "partial_scores": dict(),
        "score": 0.0,
        "feedback": dict(),
        "variant_seed": 0,
        "options": dict(),
        "raw_submitted_answers": dict(),
        "editable": False,
        "panel": "question",
        "extensions": dict(),
        "ai_grading": False,
        "answers_names": dict(),
        "num_valid_submissions": 0,
        "manual_grading": False
    }

    return data

class VerifyFormStringFromShorthand:
    @pytest.mark.parametrize(
        "shorthand",
        [
            "",
            "abcdefg",
            "0abc1^{2}",
            "1^}",
            "1^{{2}",
            "0^{1}0^{1}}",
            "abc0" "0abc",
            "1^{1a2}",
            "0^{-1}",
            "2^{12}",
        ],
    )
    def verify_malformed_input(self, shorthand: str) -> None:
        with pytest.raises(ValueError):
            su.form_string_from_shorthand(shorthand)

    @pytest.mark.parametrize(
        "shorthand,expected",
        [
            ("e", ""),
            ("01", "01"),
            ("0^{200}", "0" * 200),
            ("00^{200}", "0" * 201),
            ("0^{5}1^{4}", "000001111"),
            ("1^{20}00^{20}", "1" * 20 + "0" * 21),
            ("1^{3}0^{5}1^{4}", "111000001111"),
        ],
    )
    def verify_correct_conversion(self, shorthand: str, expected: str) -> None:
        assert su.form_string_from_shorthand(shorthand) == expected


@pytest.mark.parametrize(
    "n,base,expected",
    [
        (1, 2, True),
        (2, 2, True),
        (5, 2, False),
        (25, 2, False),
        (8, 2, True),
        (64, 2, True),
        (64, 3, False),
        (25, 5, True),
        (125, 5, True),
    ],
)
def verify_is_power_of_base(n: int, base: int, expected: bool) -> None:
    assert su.is_power_of_base(n, base) == expected


@pytest.mark.parametrize(
    "n,power,expected",
    [
        (1, 2, True),
        (2, 2, False),
        (5, 2, False),
        (25, 2, True),
        (56, 2, False),
        (64, 2, True),
        (27, 3, True),
        (81, 3, False),
    ],
)
def verify_is_perfect_power(n: int, power: int, expected: bool) -> None:
    assert su.is_perfect_power(n, power) == expected


@pytest.mark.parametrize(
    "question_name, student_answer, feedback_field, weight, expected_grade",
    [
        ("base", "a", "base", 1, True),
        ("base", "a, b", "base", 1, False),
        ("base", "", "home", 2, False),
        ("home", "b", "base", 2, True),
        ("base", "c", None, 3, True),
        ("base", "<>", None, 3, True),
        ("base", "><", None, 3, False),
    ],
)
def verify_grade_question_parametrized_correct(
    question_name: str,
    student_answer: str,
    feedback_field: Optional[str],
    weight: int,
    expected_grade: bool,
) -> None:
    data: su.QuestionData = qdata()
    data["partial_scores"] = dict()
    data["submitted_answers"] = {question_name: student_answer}
    data["feedback"] = dict()
    good_feedback = " you did good"
    bad_feedback = "thats terrible"

    def grading_function(submitted_answer: str) -> tuple[bool, Optional[str]]:
        if submitted_answer in {"a", "b", "c", "d", "<>"}:
            return True, good_feedback
        return False, bad_feedback

    su.grade_question_parameterized(
        data, question_name, grading_function, weight, feedback_field
    )

    if feedback_field is None:
        feedback_field = question_name

    expected_score = 1.0 if expected_grade else 0.0
    assert su.get_partial_score(data, question_name) == expected_score
    assert type(su.get_partial_score(data, question_name)) is float
    assert data["partial_scores"][question_name]["weight"] == weight # type: ignore

    expected_feedback = good_feedback if expected_grade else bad_feedback

    assert data["feedback"][feedback_field] == expected_feedback
    assert data["partial_scores"][question_name]["feedback"] == expected_feedback # type: ignore


@pytest.mark.parametrize(
    "student_ans, should_raise",
    [("<evil javascript>", True), ("><", True), ("a < b", False), ("b > a", False)],
)
def verify_grade_question_parametrized_exception(
    student_ans: str, should_raise: bool
) -> None:
    question_name = "name"

    data = qdata()
    data["partial_scores"] = dict()
    data["submitted_answers"] = {question_name: student_ans}
    data["feedback"] = dict()

    def grading_function(ans: str) -> tuple[bool, Optional[str]]:
        return True, f"The answer {ans} is right"

    if should_raise:
        with pytest.raises(ValueError, match="input should not be present"):
            su.grade_question_parameterized(
                data, question_name, grading_function
            )
    else:
        su.grade_question_parameterized(data, question_name, grading_function)

        assert su.get_partial_score(data, question_name) == 1


def verify_grade_question_parametrized_bad_grade_function() -> None:
    question_name = "name"

    data = qdata()
    data["partial_scores"] = dict()
    data["submitted_answers"] = {question_name: "True"}
    data["feedback"] = dict()

    def grading_function(ans: str):
        return "True", f"The answer {ans} is right"

    with pytest.raises(AssertionError):
        su.grade_question_parameterized(data, question_name, grading_function) #type: ignore


def verify_grade_question_parametrized_key_error_blank() -> None:
    question_name = "name"

    data = qdata()
    data["partial_scores"] = dict()
    data["submitted_answers"] = {question_name: "True"}
    data["feedback"] = dict()

    def grading_function(ans: str) -> tuple[bool, Optional[str]]:
        decoy_dict: dict[str, str] = dict()
        decoy_dict["junk"]  # This is to throw a key error
        return (True, None)

    with pytest.raises(KeyError):
        su.grade_question_parameterized(data, question_name, grading_function)

    # Empty out submitted answers
    data["submitted_answers"] = dict()
    data["format_errors"] = dict()
    su.grade_question_parameterized(data, question_name, grading_function)

    assert data["format_errors"][question_name] == "No answer was submitted"


@pytest.mark.parametrize(
    "expected_answer, student_answer, expected_grade, weight",
    [
        ("(1, 2, 3), (4, 5)", "(4, 5), (1, 2, 3)", 1, 1),
        ("(1, 2), 3, (4, 5)", "(4, 5), (1, 2, 3)", 0, 2),
        ("(1, 2), (3), (4, 5)", "(3), (4, 5), (2, 1)", 0, 1),
        ("(1, 2, 3), (4, 5), (3)", "(1, 2, 3), (4, 5), (3)", 1, 1),
        ("{(1, 2, 3), (4, 5), (3)}", "(1, 2, 3), (4, 5), (3)", 0, 1),
        ("(1, 2, 3), (4, 5), (3)", "{(1, 2, 3), (4, 5), (3)}", 0, 1),
        ("{(1, 2, 3), (3), (4, 5)}", "{(3), (1, 2, 3), (4, 5)}", 1, 1),
        ("∅", "∅", 1, 1),
        ("∅", "{}", 1, 1),
        # cases w/ unicode characters
        ("\uff081, 2, 3), (4, 5\uff09", "(4, 5), (1, 2, 3)", 1, 1),
        ("\ufe59 1, 2, 3), (4, 5), (3 )", "(1, 2, 3), (4, 5), (3)", 1, 1),
        ("{(1, 2, 3), (4\u066b 5), (3)}", "(1, 2, 3), (4, 5), (3)", 0, 1),
        ("(1, 2, 3), (4, 5), (3)", "\ufe5b(1, 2, 3), (4, 5), (3)}", 0, 1),
    ],
)
def verify_grade_question_tokenized(
    expected_answer: str, student_answer: str, expected_grade: int, weight: int
) -> None:
    data = qdata()
    data["partial_scores"] = dict()
    data["submitted_answers"] = {"base": student_answer}
    data["format_errors"] = dict()
    data["format_errors"]["base"] = None
    is_expected_answer_set = (
        expected_answer.startswith("{")
        and expected_answer.endswith("}")
        or expected_answer == "∅"
    )
    is_student_answer_with_braces = student_answer.startswith(
        "{"
    ) or student_answer.startswith("}")
    is_student_answer_set = is_student_answer_with_braces or student_answer == "∅"

    su.grade_question_tokenized(data, "base", expected_answer, weight)
    if (
        is_expected_answer_set
        and not is_student_answer_with_braces
        and not is_student_answer_set
    ):
        # Verify error handling of not using set braces when expected
        assert (
            data["format_errors"]["base"]
            == "Make sure to format your answer with curly braces to denote a set"
        )
    elif not is_expected_answer_set and is_student_answer_with_braces:
        # Verify error handling of using set braces when not expected
        assert (
            data["format_errors"]["base"]
            == "This input field is not a set, so it does not require curly braces"
        )

    assert data["partial_scores"]["base"]["weight"] == weight #type: ignore
    assert su.get_partial_score(data, "base") == expected_grade


@pytest.mark.parametrize(
    "expected_feedback, student_answer",
    [
        ("Binary 0", ("0", "0", "0")),
        ("", ("0", "0", "1")),
        ("At least 2", ("0", "1", "0")),
        ("At least 2", ("0", "1", "1")),
        ("Binary 4", ("1", "0", "0")),
        ("Binary 5", ("1", "0", "1")),
        ("At least 2", ("1", "1", "0")),
        ("At least 2", ("1", "1", "1")),
    ],
)
def verify_set_holistic_feedback(
    expected_feedback: str, student_answer: tuple[str, str, str]
) -> None:
    data = qdata()
    data["partial_scores"] = {"p1": {"score": 0}, "p2": {"score": 0}, "p3": {"score": 0}}
    data["submitted_answers"] = {
        "p1": student_answer[0],
        "p2": student_answer[1],
        "p3": student_answer[2],
    }
    data["feedback"] = dict()
    data["feedback"]["fb"] = ""

    def test_feedback(p1: str, p2: str, p3: str) -> Optional[str]:
        if p1 == "0" and p2 == "0" and p3 == "0":
            return "Binary 0"
        elif p1 == "1" and p2 == "0" and p3 == "0":
            return "Binary 4"
        elif p2 == "1":
            return "At least 2"
        elif p1 == "1" and p2 == "1":
            return "This feedback should never be returned"
        elif p1 == "1" and p2 == "0" and p3 == "1":
            return "Binary 5"
        else:
            return None

    su.set_holistic_feedback(data, "fb", test_feedback)

    assert data["feedback"]["fb"] == expected_feedback


@pytest.mark.parametrize(
    "expected_sentence, list_of_str",
    [
        ("", []),
        ("i", ["i"]),
        ("foo and bar", ["foo", "bar"]),
        ("foo", ["foo"]),
        ("foo:a, bar:b, and baz:c", ["foo:a", "bar:b", "baz:c"]),
        ("foo, bar, and baz", ["foo", "bar", "baz"]),
        ("a, b, c, and d", ["a", "b", "c", "d"]),
    ],
)
def verify_list_to_english(expected_sentence: str, list_of_str: list[str]) -> None:
    assert su.list_to_english(list_of_str) == expected_sentence
