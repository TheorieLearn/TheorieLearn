from typing import Any, Dict, List, Optional, Tuple

import pytest
import theorielearn.shared_utils as su
import sympy
from pytest_mock import MockerFixture

QUESTION_NAME = "Q"


@pytest.fixture
def grader(mocker: MockerFixture):
    class MockHasInvalidFunctionError(Exception):
        def __init__(self, text):
            self.text = text

    class MockHasInvalidVariableError(Exception):
        def __init__(self, text):
            self.text = text

    class MockHasEscapeError(Exception):
        pass

    class MockHasCommentError(Exception):
        pass

    def mock_evaluate(input_str: str, ns: Dict[str, Dict[str, Any]]):
        expr = sympy.sympify(input_str, locals=ns)

        functions_dict = ns["functions"]
        vars_dict = ns["variables"]

        for func_obj in expr.atoms(sympy.Function):
            func_name = str(func_obj.func)

            if func_name not in functions_dict:
                raise MockHasInvalidFunctionError(func_name)

        for var_obj in expr.atoms(sympy.Symbol):
            var_name = str(var_obj)

            if var_name not in vars_dict:
                raise MockHasInvalidVariableError(var_name)

        return expr

    mock_import = mocker.MagicMock()
    mock_import.evaluate = mock_evaluate

    mock_import.HasInvalidFunctionError = MockHasInvalidFunctionError
    mock_import.HasInvalidVariableError = MockHasInvalidVariableError
    mock_import.HasEscapeError = MockHasEscapeError
    mock_import.HasCommentError = MockHasCommentError

    mocker.patch.dict("sys.modules", python_helper_sympy=mock_import)
    from theorielearn.sympy_utils.utils import SympyGrader

    local_functions = {"MinCost": 1, "HotelCosts": 1}
    local_variables = {"i", "n", "j", "k"}

    return SympyGrader(QUESTION_NAME, local_functions, local_variables)


@pytest.fixture
def data() -> su.QuestionData:
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


@pytest.mark.parametrize(
    "invalid_answer",
    [
        "4n",
        "4n/3",
        "i j",
        "(i))",
        "((i)/2",
        "MinCost(i/2, i)",
        "MinCost",
        "i()",
        "f()",
        "f",
    ],
)
def verify_grade_question_answer_exception(
    grader, data: Dict[str, Dict[str, Any]], invalid_answer: str
) -> None:
    data["submitted_answers"] = {QUESTION_NAME: "n"}

    with pytest.raises(ValueError):
        grader.grade_question(data, invalid_answer)


@pytest.mark.parametrize(
    "student_answer",
    ["4n / 4", "4n", "(n))", "((n)/2", "MinCost(i/2, i)", "MinCost", "i()", "f()", "f"],
)
def verify_grade_question_format_error(
    grader, data: su.QuestionData, student_answer: str
) -> None:
    data["submitted_answers"] = {QUESTION_NAME: student_answer}

    grader.grade_question(data, "n")

    assert type(data["format_errors"][QUESTION_NAME]) is str
    assert data["format_errors"][QUESTION_NAME] != ""
    assert su.get_partial_score(data, QUESTION_NAME) == 0


@pytest.mark.parametrize(
    "student_answer, correct_answers, substitutions, expected_grade",
    [
        ("4**n+2", ["2+(4**n)", "n**2"], None, 1),
        ("n * n", ["2+(4**n)", "n**2"], None, 1),
        ("n * 3", ["2+(4**n)", "n**2"], None, 0),
        ("2 * n", ["i / 2"], [("n", "i / 4")], 1),
        ("2 * n", ["i / 2"], [("n", "i / 3")], 0),
        ("MinCost(i/2)", ["HotelCosts(n)"], [("MinCost(i/2)", "HotelCosts(n)")], 1),
        ("MinCost(2 * n)", ["MinCost(2 * n * log(n))"], None, 0),
        ("log(i)", ["i"], None, 0),
    ],
)
def verify_grade_question_correct(
    grader,
    data: su.QuestionData,
    student_answer: str,
    correct_answers: List[str],
    substitutions: Optional[List[Tuple[str, str]]],
    expected_grade: int,
) -> None:
    data["submitted_answers"] = {QUESTION_NAME: student_answer}

    if not substitutions:
        grader.grade_question(data, *correct_answers)
    else:
        grader.grade_question(data, *correct_answers, substitutions=substitutions)

    assert su.get_partial_score(data, QUESTION_NAME) == expected_grade


@pytest.mark.parametrize(
    "student_answer, should_have_feedback",
    [
        ("HotelCosts(n)", True),
        ("MinCost(HotelCosts(n))", False),
        ("HotelCosts(MinCost(i))", False),
        ("MinCost(i)", False),
    ],
)
def verify_grade_question_missing_function(
    grader, data: su.QuestionData, student_answer: str, should_have_feedback: bool
) -> None:
    """
    Check that feedback is set when function is missing
    """

    unique_feedback = "You should use this function"
    grader.answer_not_includes_function_feedback("MinCost", unique_feedback)

    data["submitted_answers"] = {QUESTION_NAME: student_answer}

    # Check that grader adds custom feedback
    grader.grade_question(data, "MinCost(n)")
    assert su.get_partial_score(data, QUESTION_NAME) == 0.0

    if should_have_feedback:
        assert data["feedback"][QUESTION_NAME] == unique_feedback
    else:
        assert QUESTION_NAME not in data["feedback"]


@pytest.mark.parametrize(
    "student_answer, should_have_feedback",
    [
        ("HotelCosts(n)", False),
        ("MinCost(HotelCosts(n))", True),
        ("HotelCosts(MinCost(i))", True),
        ("MinCost(i)", True),
    ],
)
def verify_grade_question_includes_function(
    grader, data: su.QuestionData, student_answer: str, should_have_feedback: bool
) -> None:
    """
    Check that feedback is set when function is included
    """
    unique_feedback = "You should not use this function"
    grader.answer_includes_function_feedback("MinCost", unique_feedback)

    data["submitted_answers"] = {QUESTION_NAME: student_answer}

    # Check that grader adds custom feedback
    grader.grade_question(data, "MinCost(n)")
    assert su.get_partial_score(data, QUESTION_NAME) == 0.0

    if should_have_feedback:
        assert data["feedback"][QUESTION_NAME] == unique_feedback
    else:
        assert QUESTION_NAME not in data["feedback"]


@pytest.mark.parametrize(
    "student_answer, should_have_feedback",
    [
        ("HotelCosts(n)", True),
        ("HotelCosts(MinCost(i))", False),
        ("MinCost(HotelCosts(n))", True),
        ("HotelCosts(i)", False),
    ],
)
def verify_grade_question_function_with_argument(
    grader, data: su.QuestionData, student_answer: str, should_have_feedback: bool
) -> None:
    """
    Check that feedback is set when function is called with argument
    """

    unique_feedback = "You should not call this function in this way"
    grader.answer_function_with_argument_feedback("HotelCosts", "n", unique_feedback)

    data["submitted_answers"] = {QUESTION_NAME: student_answer}

    # Check that grader adds custom feedback
    grader.grade_question(data, "MinCost(n)")

    assert su.get_partial_score(data, QUESTION_NAME) == 0.0

    if should_have_feedback:
        assert data["feedback"][QUESTION_NAME] == unique_feedback
    else:
        assert QUESTION_NAME not in data["feedback"]


@pytest.mark.parametrize(
    "student_answer, should_have_feedback",
    [
        ("HotelCosts(n)", False),
        ("MinCost(HotelCosts(n))", False),
        ("HotelCosts(i)", True),
        ("HotelCosts(MinCost(i))", True),
        ("MinCost(HotelCosts(i))", True),
    ],
)
def verify_grade_question_function_without_argument(
    grader, data: su.QuestionData, student_answer: str, should_have_feedback: bool
) -> None:
    """
    Check that feedback is set when function is called without argument
    """

    unique_feedback = "You should call this function in this way"
    grader.answer_function_without_argument_feedback("HotelCosts", "n", unique_feedback)

    data["submitted_answers"] = {QUESTION_NAME: student_answer}

    # Check that grader adds custom feedback
    grader.grade_question(data, "MinCost(n)")
    assert su.get_partial_score(data, QUESTION_NAME) == 0.0

    if should_have_feedback:
        assert data["feedback"][QUESTION_NAME] == unique_feedback
    else:
        assert QUESTION_NAME not in data["feedback"]


def verify_grade_question_feedback_exceptions(grader, data: su.QuestionData) -> None:
    unique_feedback = "test"

    # Exceptions raised for invalid function used
    with pytest.raises(ValueError):
        grader.answer_not_includes_function_feedback("f", unique_feedback)

    with pytest.raises(ValueError):
        grader.answer_includes_function_feedback("f", unique_feedback)

    with pytest.raises(ValueError):
        grader.answer_function_with_argument_feedback("f", "n", unique_feedback)

    with pytest.raises(ValueError):
        grader.answer_function_without_argument_feedback("f", "n", unique_feedback)

    data["submitted_answers"] = {QUESTION_NAME: "HotelCosts(i)"}
    grader.grade_question(data, "MinCost(n)")

    # Exceptions raised for trying to add feedback for a graded question or grading again
    with pytest.raises(ValueError):
        grader.grade_question(data, "MinCost(n)")

    with pytest.raises(ValueError):
        grader.answer_not_includes_function_feedback("HotelCosts", unique_feedback)

    with pytest.raises(ValueError):
        grader.answer_includes_function_feedback("HotelCosts", unique_feedback)

    with pytest.raises(ValueError):
        grader.answer_function_with_argument_feedback(
            "HotelCosts", "n", unique_feedback
        )

    with pytest.raises(ValueError):
        grader.answer_function_without_argument_feedback(
            "HotelCosts", "n", unique_feedback
        )
