from typing import Any, Callable, Dict, Optional, Tuple

import chevron
import prairielearn as pl
import theorielearn.shared_utils as su
from theorielearn.shared_utils import grade_question_parameterized


def render_suffix_string(suffix: str) -> str:
    """
    Creates a displayable version of a user-supplied distinguishing suffix.
    @param suffix string
        user-supplied suffix
    @return string
        '\\varepsilon' if suffix is 'e' (for epsilon), suffix otherwise.
    """
    if suffix == "e":
        return "\\varepsilon"
    return suffix


def render_result_string(prefix: str, suffix: str) -> str:
    """
    Creates a displayable version of the concatenation of a question-generated prefix and a user-supplied suffix.
    @param prefix string
        question-generated prefix
    @param suffix string
        user-supplied suffix
    @return string
        concatenation of prefix and suffix if concatenation is nonempty, '\\varepsilon' otherwise
    """
    if prefix == "\\varepsilon":
        prefix = ""
    if suffix == "e":
        suffix = ""
    if prefix + suffix == "":
        return "\\varepsilon"
    return prefix + suffix


def determine_suffix_correctness(
    distinguishing_suffix: str,
    is_in_language: Callable[[str], bool],
    first_prefix: str,
    second_prefix: str,
    rendered_first_prefix: str,
    rendered_second_prefix: str,
) -> Tuple[bool, Optional[str]]:
    """
    Determines whether distinguishing suffix is correct.
    @param distinguishing_suffix str
        distinguishing suffix to check
    @param is_in_language Callable[[str], bool]
        function that determines language membership
    @param first_prefix str
        first prefix
    @param second_prefix str
        second prefix
    @param rendered_first_prefix str
        first prefix in format to be shown to user
    @param rendered_second_prefix str
        second prefix in format to be shown to user
    @return tuple[bool, Optional[str]]
        The first element of the return tuple is a boolean indicating whether the answer was correct
        (True for correct, False for incorrect)
        The second element of the return tuple is an optional string
        that gives feedback on the issue with the submission.
    """

    # Clean distinguishing suffix
    cleaned_distinguishing_suffix = distinguishing_suffix.replace(" ", "")

    # Render distinguishing suffix and other strings
    rendered_distinguishing_suffix = render_suffix_string(cleaned_distinguishing_suffix)

    rendered_first_string = render_result_string(
        rendered_first_prefix, cleaned_distinguishing_suffix
    )

    rendered_second_string = render_result_string(
        rendered_second_prefix, cleaned_distinguishing_suffix
    )

    # Check correctness
    expanded_suffix = su.form_string_from_shorthand(
        cleaned_distinguishing_suffix
    )
    first_string_in_language = is_in_language(first_prefix + expanded_suffix)
    second_string_in_language = is_in_language(second_prefix + expanded_suffix)

    # Give feedback
    if first_string_in_language != second_string_in_language:
        return True, (
            f"${rendered_distinguishing_suffix}$ is a distinguishing suffix for "
            f"${rendered_first_prefix}$ and ${rendered_second_prefix}$!"
        )
    elif first_string_in_language and second_string_in_language:
        return (
            False,
            f"Both ${rendered_first_string}$ and ${rendered_second_string}$ are in the language.",
        )
    else:
        return (
            False,
            f"Neither ${rendered_first_string}$ nor ${rendered_second_string}$ is in the language.",
        )


def grade(data: pl.QuestionData, is_in_language: Callable[[str], bool]) -> None:
    params = data["params"]

    grade_question_parameterized(
        data,
        "distinguishing_suffix",
        lambda x: determine_suffix_correctness(
            x,
            is_in_language,
            params["fooling_set_member_1"],
            params["fooling_set_member_2"],
            params["fooling_set_member_1_display"],
            params["fooling_set_member_2_display"],
        ),
        feedback_field_name="suffix",
    )

    pl.set_weighted_score_data(data)


def generate(data: Dict) -> None:
    with open(
        data["options"]["server_files_course_path"]
        + "/theorielearn/fooling_set_drill/question_base.html"
    ) as f:
        data["params"]["html"] = chevron.render(f, data).strip()
