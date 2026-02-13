import html
import json
from enum import Enum
from typing import List

import chevron
import lxml.html
import prairielearn as pl
from prairielearn import QuestionData

SCAFFOLDED_WRITING_MUSTACHE_TEMPLATE_NAME = "tl-scaffolded-writing.mustache"
class Type(Enum):
    DP = "isDP"
    GRAPH = "isGraph"


class Sort(Enum):
    NONE = "none"
    ASCENDING = "ascending"
    DESCENDING = "descending"


def assemble_response(tokens: List[str]) -> str:
    """
    Combines tokens into a single string that can be displayed to the student.

    Tokens will be separated by a space, but there will be no space immediately preceding a comma or period.
    Tokens that appear at the start of the response or immediately after a period will have their first
    letter automatically capitalized.
    """
    response: List[str] = []

    for token in tokens:
        should_capitalize = not response or response[-1] == "."

        if response and token not in {",", "."}:
            response.append(" ")

        if should_capitalize:
            response.append(token[:1].upper() + token[1:])
        else:
            response.append(token)

    return "".join(response)


def prepare(element_html: str, data: QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)
    required_attribs = ["answers-name"]
    optional_attribs: List[str] = ["type", "sort"]
    pl.check_attribs(element, required_attribs, optional_attribs)

    name = pl.get_string_attrib(element, "answers-name")

    if f"{name}_cfg" not in data["params"]:
        raise Exception(f"CFG was not provided for tl-scaffolded-writing element: {name}")


def render(element_html: str, data: QuestionData) -> str:
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, "answers-name")
    type = pl.get_enum_attrib(element, "type", Type, Type.DP)
    sort = pl.get_enum_attrib(element, "sort", Sort, Sort.NONE)

    editable = data["editable"]

    entered_tokens: List[str] = data["submitted_answers"].get(name, [])
    entered_tokens = [html.escape(token) for token in entered_tokens]

    if data["panel"] == "question":
        with open(SCAFFOLDED_WRITING_MUSTACHE_TEMPLATE_NAME, "r") as f:
            return chevron.render(
                f,
                {
                    "answers_name": name,
                    "entered_tokens": json.dumps(entered_tokens),
                    "cfg": data["params"][f"{name}_cfg"],
                    "editable": editable,
                    type.value: True,
                    "sort_type": sort.value,
                },
            ).strip()

    elif data["panel"] == "submission":
        feedback_paragraphs = []

        if entered_tokens:
            feedback_paragraphs.append(
                f"<p><b>Your response:</b> {assemble_response(entered_tokens)}</p>"
            )

        if name in data["format_errors"]:
            feedback_paragraphs.append(
                f"<p><b>Error:</b> {data['format_errors'][name]}</p>"
            )

        if name in data["feedback"]:
            feedback_paragraphs.append(
                f"<p><b>Feedback:</b> {data['feedback'][name]}</p>"
            )

        return f"""
            <div class="tl-scaffolded-writing-submission">
                {''.join(feedback_paragraphs)}
            </div>
        """

    else:  # answer panel
        return "There may be more than one correct answer. If your answer was marked incorrect, please use the feedback provided below to improve your answer."


def parse(element_html: str, data: QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, "answers-name")

    if data["raw_submitted_answers"].get(name) is None:
        data["format_errors"][name] = (
            "Format error: None was received when attempting to read answer."
        )
        return

    entered_tokens: List[str] = json.loads(data["raw_submitted_answers"][name])
    entered_tokens = [html.unescape(token) for token in entered_tokens]

    if len(entered_tokens) == 0:
        data["format_errors"][name] = "You cannot save an empty response."

    data["submitted_answers"][name] = entered_tokens
