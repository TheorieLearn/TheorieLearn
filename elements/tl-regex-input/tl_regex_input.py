"""Python controller for regex input element."""

import json
from typing import Optional, Tuple

import chevron
import lxml.html
import prairielearn as pl
from automata.fa.dfa import DFA
from fa_utils import generate_dfa_feedback_html
from json_utils import dfa_dump_json, dfa_from_json
from regular_expressions.exceptions import RegexException
from regular_expressions.parser import compute_nfa_from_regex_lines
from typing_extensions import assert_never

ALPHABET_DEFAULT = "01"
WEIGHT_DEFAULT = 1
MAX_LENGTH_TO_CHECK = 10

REGEX_INPUT_MUSTACHE_TEMPLATE_NAME = "tl-regex-input.mustache"


def prepare(element_html: str, data: pl.QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)
    required_attribs = ["answers-name"]
    optional_attribs = ["weight", "alphabet"]

    # Get attributes
    pl.check_attribs(element, required_attribs, optional_attribs)
    name = pl.get_string_attrib(element, "answers-name")
    alphabet_str = pl.get_string_attrib(element, "alphabet", ALPHABET_DEFAULT)

    # Parse alphabet string into set
    alphabet = set(alphabet_str)

    if len(alphabet) != len(alphabet_str):
        raise ValueError(
            f"Alphabet string '{alphabet_str}' must have all distinct characters."
        )

    # Try parsing correct answer, will raise exception if not defined correctly
    correct_regex = element.text

    if correct_regex is not None:
        equiv_nfa = compute_nfa_from_regex_lines(correct_regex, alphabet)
        correct_answer_dfa = dfa_dump_json(
            (DFA.from_nfa(equiv_nfa, retain_names=False, minify=True)).to_complete()
        )

        if name in data["correct_answers"]:
            raise Exception(f"Duplicate correct_answers variable name: {name}")

        data["correct_answers"][name] = json.dumps(correct_answer_dfa)

    if name not in data["correct_answers"]:
        raise Exception(f"No correct answer provided for {name}")


def render(element_html: str, data: pl.QuestionData) -> str:
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, "answers-name")
    alphabet = sorted(pl.get_string_attrib(element, "alphabet", ALPHABET_DEFAULT))
    submitted_answer = data["submitted_answers"].get(name, "")

    submission_was_correct = None
    counterexample_strings = None
    did_submit_answer = name in data["partial_scores"]

    if did_submit_answer:
        submission_was_correct = data["partial_scores"][name].get("score", 0.0) == 1.0
        counterexample_strings = data["partial_scores"][name].get("feedback", None)

    alphabet_list = [{"char": char, "last": False} for char in alphabet]
    alphabet_list[-1]["last"] = True

    if data["panel"] == "question":
        with open(REGEX_INPUT_MUSTACHE_TEMPLATE_NAME, "r", encoding="utf-8") as f:
            help_text = chevron.render(
                f,
                {
                    "help_text_body": True,
                    "alphabet_list": alphabet_list,
                    "alphabet_union": "+".join(alphabet),
                },
            ).strip()

        editable = data["editable"]
        html_params = {
            "question": True,
            "name": name,
            "submitted_answer": submitted_answer,
            "display_score_badge": did_submit_answer,
            "correct": submission_was_correct,
            "editable": editable,
            "help_text": help_text,
        }

        with open(REGEX_INPUT_MUSTACHE_TEMPLATE_NAME, "r", encoding="utf-8") as f:
            return chevron.render(f, html_params).strip()

    elif data["panel"] == "submission":
        submitted_answer_lines = [
            {"answer_line": input_line} for input_line in submitted_answer.splitlines()
        ]

        html_params = {
            "submission": True,
            "submitted_answer_lines": submitted_answer_lines,
            "parse_errors": data["format_errors"].get(name, None),
            "submission_was_graded": submission_was_correct is not None,
            "submission_was_correct": submission_was_correct,
            "counterexample_strings": counterexample_strings,
        }

        with open(REGEX_INPUT_MUSTACHE_TEMPLATE_NAME, "r", encoding="utf-8") as f:
            return chevron.render(f, html_params).strip()

    # Nothing interesting to display in correct answer panel, should just hide
    elif data["panel"] == "answer":
        return ""

    assert_never(data["panel"])


def grade(element_html: str, data: pl.QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)

    weight = pl.get_integer_attrib(element, "weight", WEIGHT_DEFAULT)
    question_name = pl.get_string_attrib(element, "answers-name")
    alphabet = set(pl.get_string_attrib(element, "alphabet", ALPHABET_DEFAULT))

    reference_equiv_dfa = dfa_from_json(
        json.loads(data["correct_answers"][question_name])
    )

    def grade_regex(student_ans: str) -> Tuple[bool, Optional[str]]:
        try:
            student_equiv_dfa = DFA.from_nfa(
                compute_nfa_from_regex_lines(student_ans, alphabet), retain_names=False
            ).to_complete()
        except RegexException as e:
            raise ValueError(str(e))

        if student_equiv_dfa == reference_equiv_dfa:
            return (True, None)

        return (
            False,
            generate_dfa_feedback_html(
                student_equiv_dfa,
                reference_equiv_dfa,
                MAX_LENGTH_TO_CHECK,
                "regular expression",
            ),
        )

    try:
        pl.grade_answer_parameterized(data, question_name, grade_regex, weight=weight)
    except ValueError as e:
        data["format_errors"][question_name] = str(e)
