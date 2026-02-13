import html
import json
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import chevron
import json_utils as ju
import lxml.html
import prairielearn as pl
from automata.fa.dfa import DFA
from grading_utils import compute_partial_credit, generate_dfa_feedback_html
from typing_extensions import assert_never

if TYPE_CHECKING:
    from automata.fa.fa import FA


ALPHABET_DEFAULT = "01"
EPSILON_SYMBOL_DEFAULT = "e"
MAX_LENGTH_TO_CHECK_DEFAULT = 10
WEIGHT_DEFAULT = 1
MAX_STATE_SCORE_SCALING_DEFAULT = 0.5

FSM_BUILDER_MUSTACHE_TEMPLATE_NAME = "tl-fsm-builder.mustache"


# TODO change these to a attributes on the element if needed
MAX_NUM_TO_CHECK = 10


def prepare(element_html: str, data: pl.QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)
    required_attribs = ["answers-name", "fsm-type"]
    optional_attribs = [
        "weight",
        "alphabet",
        "epsilon-symbol",
        "max-check-length",
        "max-state-score-scaling",
    ]
    pl.check_attribs(element, required_attribs, optional_attribs)

    name = pl.get_string_attrib(element, "answers-name")
    epsilon_symbol = pl.get_string_attrib(
        element, "epsilon-symbol", EPSILON_SYMBOL_DEFAULT
    )

    if len(epsilon_symbol) != 1:
        raise ValueError(
            f"Epsilon symbol must be a single character, not '{epsilon_symbol}'."
        )

    max_length_to_check = pl.get_integer_attrib(
        element, "max-check-length", MAX_LENGTH_TO_CHECK_DEFAULT
    )

    if max_length_to_check < 1:
        raise ValueError(
            f"max-check-length must be at least 1, not {max_length_to_check}."
        )

    max_state_score_scaling = pl.get_float_attrib(
        element,
        "max-state-score-scaling",
        MAX_STATE_SCORE_SCALING_DEFAULT,
    )

    if not (0.0 <= max_state_score_scaling <= 1.0):
        raise ValueError(
            f"max-state-score-scaling must be between 0.0 and 1.0, not {max_state_score_scaling}."
        )

    fsm_type_name = pl.get_string_attrib(element, "fsm-type").upper()
    fsm_type = ju.FSMType[fsm_type_name]

    if fsm_type is ju.FSMType.DFA and pl.has_attrib(element, "epsilon-symbol"):
        raise ValueError(
            "Attribute `epsilon-symbol` should not be set if FSM type is DFA."
        )

    alphabet_list = list(pl.get_string_attrib(element, "alphabet", ALPHABET_DEFAULT))

    if any(alphabet_element.isspace() for alphabet_element in alphabet_list):
        raise ValueError("Alphabet string contains whitespace.")

    # Parse alphabet string into set
    alphabet = ju.list_as_set(alphabet_list)

    # Initialize dictionary
    data["params"][name] = {}

    # If element text is present, load for grading
    for child in element:
        if child.tag in {"correct-answer", "pl-correct-answer"}:
            # Record max states
            pl.check_attribs(
                child, required_attribs=[], optional_attribs=["max-states"]
            )

            if pl.has_attrib(child, "max-states"):
                data["params"][name]["max_states"] = pl.get_integer_attrib(
                    child, "max-states"
                )

            # Don't use PL helper function, because we need un-escaped input
            reference_fsm_dict = json.loads(str(child.text))

            # Serialize so we check for validity, will raise exception if invalid
            if fsm_type is ju.FSMType.DFA:
                ref_dfa = ju.dfa_from_json(reference_fsm_dict)
                assert ref_dfa.input_symbols == alphabet
            elif fsm_type is ju.FSMType.NFA:
                ref_nfa = ju.nfa_from_json(reference_fsm_dict)
                assert ref_nfa.input_symbols == alphabet
            else:
                assert_never(fsm_type)

            data["correct_answers"][name] = json.dumps(reference_fsm_dict)
        else:
            raise ValueError(f"Unsupported child tag name '{child.tag!s}'")

    # Add epsilon symbol if in NFA mode
    if fsm_type is ju.FSMType.NFA:
        if epsilon_symbol in alphabet_list:
            raise ValueError(
                f"Alphabet list {alphabet_list} contains epsilon symbol: '{epsilon_symbol}'"
            )
        alphabet_list.append(epsilon_symbol)

    # Save parameters to data dict
    data["params"][name]["fsm_type_name"] = fsm_type_name
    data["params"][name]["alphabet_list"] = alphabet_list


def render(element_html: str, data: pl.QuestionData) -> str:
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, "answers-name")
    epsilon_symbol = pl.get_string_attrib(
        element, "epsilon-symbol", EPSILON_SYMBOL_DEFAULT
    )
    fsm_type = ju.FSMType[data["params"][name]["fsm_type_name"]]
    alphabet_list = data["params"][name]["alphabet_list"]

    editable = data["editable"]
    display_dict_name = f"{name}-raw"
    display_json = data["submitted_answers"].get(display_dict_name, None)

    if data["panel"] == "question":
        html_params : dict[str, Any] = {
            "question": True,
            "answers_name": name,
            "display_json": json.dumps(display_json),
            "alphabet_list": json.dumps(alphabet_list),
            "alphabet_chars": ", ".join(alphabet_list),
            "epsilon_symbol": epsilon_symbol,
            "format_errors_json": json.dumps(data["format_errors"].get(name, None)),
            "mode_dfa": fsm_type is ju.FSMType.DFA,
            "mode_nfa": fsm_type is ju.FSMType.NFA,
            "fsm_type_name": fsm_type.name,
            "editable": editable,
            "checked": data["submitted_answers"].get(get_checkbox_name(name), None),
            "max_states": data["params"][name].get("max_states", 0),
        }

        with open(FSM_BUILDER_MUSTACHE_TEMPLATE_NAME) as f:
            return chevron.render(f, html_params).strip()
    elif data["panel"] == "submission":
        html_params = {"submission": True}

        if name in data["format_errors"]:
            html_params["parse_errors"] = data["format_errors"][name]

        # If no format errors, get feedback
        elif name in data["partial_scores"]:
            html_params["feedback"] = data["partial_scores"][name].get("feedback", None)

            fsm_json_dict = json.loads(data["submitted_answers"][name])

            if fsm_type is ju.FSMType.DFA:
                student_fsm: FA = ju.dfa_from_json(fsm_json_dict)
            elif fsm_type is ju.FSMType.NFA:
                student_fsm = ju.nfa_from_json(fsm_json_dict)
            else:
                assert_never(fsm_type)

            html_params["fsm_diagram"] = str(student_fsm.show_diagram())

        with open(FSM_BUILDER_MUSTACHE_TEMPLATE_NAME) as f:
            return chevron.render(f, html_params).strip()

    # Nothing interesting to display in correct answer panel, should just hide
    elif data["panel"] == "answer":
        if name not in data["correct_answers"]:
            return ""

        fsm_json_dict = json.loads(data["correct_answers"][name])

        if fsm_type is ju.FSMType.DFA:
            correct_fsm: FA = ju.dfa_from_json(fsm_json_dict)
        elif fsm_type is ju.FSMType.NFA:
            correct_fsm = ju.nfa_from_json(fsm_json_dict)
        else:
            assert_never(fsm_type)

        return f"<pl-graph>{correct_fsm.show_diagram()}</pl-graph>"

    assert_never(data["panel"])


def parse(element_html: str, data: pl.QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, "answers-name")
    epsilon_symbol = pl.get_string_attrib(
        element, "epsilon-symbol", EPSILON_SYMBOL_DEFAULT
    )

    try:
        fsm_json = json.loads(data["raw_submitted_answers"][f"{name}-raw"])
    except json.JSONDecodeError:
        data["format_errors"][name] = {"message": "Could not parse submission."}
        return

    checkbox_name = get_checkbox_name(name)
    data["submitted_answers"][checkbox_name] = (
        data["raw_submitted_answers"].get(checkbox_name, "off") == "on"
    )

    # Get FSM info from raw dict
    states = []
    final_states = []
    for node in fsm_json["nodes"]:
        states.append(node["text"])
        if node["isAcceptState"]:
            final_states.append(node["text"])

    transitions: dict[str, dict[str, list[str]]] = {state: {} for state in states}
    initial_states = []

    for link in fsm_json["links"]:
        if link["type"] == "StartLink":
            node = states[link["node"]]
            initial_states.append(node)

        if link["type"] == "SelfLink":
            node = states[link["node"]]

            for char in link["text"].split(","):
                transitions[node].setdefault(char, []).append(node)

        if link["type"] == "Link":
            start_node = states[link["nodeA"]]
            end_node = states[link["nodeB"]]

            for char in link["text"].split(","):
                transitions[start_node].setdefault(char, []).append(end_node)

    data["submitted_answers"][name] = json.dumps({
        "states": states,
        "input_symbols": data["params"][name]["alphabet_list"],
        "transitions": transitions,
        "initial_state": initial_states,
        "final_states": final_states,
        "include_dump_state": data["submitted_answers"][checkbox_name],
        "epsilon_symbol": epsilon_symbol,
    })


def grade(element_html: str, data: pl.QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)

    weight = pl.get_integer_attrib(element, "weight", WEIGHT_DEFAULT)
    name = pl.get_string_attrib(element, "answers-name")
    max_length_to_check = pl.get_integer_attrib(
        element, "max-check-length", MAX_LENGTH_TO_CHECK_DEFAULT
    )
    max_state_score_scaling = pl.get_float_attrib(
        element,
        "max-state-score-scaling",
        MAX_STATE_SCORE_SCALING_DEFAULT,
    )

    fsm_json = json.loads(data["submitted_answers"][name])
    fsm_type = ju.FSMType[data["params"][name]["fsm_type_name"]]

    dump_state: bool = data["submitted_answers"].get(get_checkbox_name(name), False)
    data["format_errors"].pop(name, None)

    # Serialize inputted FSM into the submitted answers dict
    try:
        if fsm_type is ju.FSMType.DFA:
            data["submitted_answers"][name] = json.dumps(
                ju.dfa_convert_json(fsm_json, dump_state=dump_state)
            )
        elif fsm_type is ju.FSMType.NFA:
            data["submitted_answers"][name] = json.dumps(ju.nfa_convert_json(fsm_json))
        else:
            assert_never(fsm_type)
    except ju.JsonValidationError as err:
        # String for highlighting
        json_transitions = (
            [
                {"startState": start_state, "char": char, "endState": end_state}
                for (start_state, char, end_state) in sorted(err.transitions)
            ]
            if err.transitions
            else None
        )

        json_states = (
            [{"name": state} for state in sorted(err.states)] if err.states else None
        )

        display_states = json_states is not None
        display_transitions = json_transitions is not None

        # If both set, only display transitions
        if display_states and display_transitions:
            display_states = False

        data["format_errors"][name] = {
            "message": err.message,
            "stateNames": json_states,
            "transitions": json_transitions,
            "displayStates": display_states,
            "displayTransitions": display_transitions,
        }

    # If we were given a reference solution, grade against that
    if name in data["correct_answers"] and name not in data["format_errors"]:
        rerference_json_string = data["correct_answers"][name]
        max_states = data["params"][name].get("max_states")

        def get_grading_info(fsm_json_string: str) -> tuple[DFA, int]:
            fsm_json_dict = json.loads(fsm_json_string)

            if fsm_type is ju.FSMType.DFA:
                dfa = ju.dfa_from_json(fsm_json_dict)
                return dfa, len(dfa.states)
            elif fsm_type is ju.FSMType.NFA:
                nfa = ju.nfa_from_json(fsm_json_dict)
                return DFA.from_nfa(nfa), len(nfa.states)
            else:
                assert_never(fsm_type)

        def grade_fsm(fsm_json_string: str) -> tuple[float, str]:
            student_equiv_dfa, num_states = get_grading_info(fsm_json_string)
            correct_equiv_dfa, _ = get_grading_info(rerference_json_string)

            if student_equiv_dfa == correct_equiv_dfa:
                if max_states is not None and num_states > max_states:
                    feedback_str = (
                        f"Your {fsm_type.name} matches the desired language, but "
                        f"has {num_states} {get_states_plural(num_states)}. "
                        f"It can have at most {max_states} {get_states_plural(max_states)} "
                        "to receive full credit.<br>"
                    )
                    return (max_state_score_scaling, feedback_str)

                return (1.0, f"Your {fsm_type.name} matches the desired language!")

            feedback_html = generate_dfa_feedback_html(
                student_equiv_dfa,
                correct_equiv_dfa,
                max_length_to_check,
                MAX_NUM_TO_CHECK,
                fsm_type.name,
            )
            partial_credit = compute_partial_credit(
                student_equiv_dfa, correct_equiv_dfa
            )

            if max_states is not None and num_states > max_states:
                feedback_str = (
                    f"Your {fsm_type.name} does not match the desired language "
                    f"and has {num_states} {get_states_plural(num_states)}{print_dump_state(fsm_type, num_states, dump_state=dump_state)}. "
                    "It must match the desired language and can have at most "
                    f"{max_states} {get_states_plural(max_states)} to receive full credit.<br>"
                )

                return (
                    partial_credit * max_state_score_scaling,
                    feedback_str + feedback_html,
                )

            feedback_str = (
                f"Your {fsm_type.name} does not match the desired language.<br>"
            )
            return (partial_credit, feedback_str + feedback_html)

        grade_question_parameterized(data, name, grade_fsm, weight=weight)


def get_checkbox_name(name: str) -> str:
    return f"{name}-include-dump-state"


def get_states_plural(num_states: int) -> str:
    return "state" if num_states == 1 else "states"


def print_dump_state(fsm_type: ju.FSMType, num_states: int, *, dump_state: bool) -> str:
    if fsm_type is ju.FSMType.NFA and dump_state:
        return f" ({num_states - 1} {get_states_plural(num_states - 1)}, plus one dump state)"
    return ""


def grade_question_parameterized(
    data: pl.QuestionData,
    question_name: str,
    grade_function: Callable[[Any], tuple[bool | float, str | None]],
    weight: int = 1,
    feedback_field_name: str | None = None,
) -> None:
    """
    Grade question question_name, marked correct if grade_function(student_answer) returns True in
    its first argument. grade_function should take in a single parameter (which will be the submitted
    answer) and return a 2-tuple.
        - The first element of the 2-tuple should either be:
            - a boolean indicating whether the question should be marked correct
            - a partial score between 0 and 1, inclusive
        - The second element of the 2-tuple should either be:
            - a string containing feedback
            - None, if there is no feedback (usually this should only occur if the answer is correct)

    Note: if the feedback_field_name is the same as the question name,
    then the feedback_field_name does not need to be specified.
    """

    # Create the data dictionary at first
    data["partial_scores"][question_name] = {"score": 0.0, "weight": weight}

    try:
        submitted_answer = data["submitted_answers"][question_name]
    except KeyError:
        # Catch error if no answer submitted
        data["format_errors"][question_name] = "No answer was submitted"
        return

    # Try to grade, exiting if there's an exception
    try:
        result, feedback_content = grade_function(submitted_answer)

        # Check _must_ be done in this order. Int check is to deal with subclass issues
        if isinstance(result, bool):
            partial_score = 1.0 if result else 0.0
        elif isinstance(result, float | int):
            assert 0.0 <= result <= 1.0
            partial_score = result
        else:
            assert_never(result)

    except ValueError as err:
        # Exit if there's a format error
        data["format_errors"][question_name] = html.escape(str(err))
        return

    # Set question score if grading succeeded
    data["partial_scores"][question_name]["score"] = partial_score

    # Put all feedback here
    if feedback_content:
        # Check for unescaped bad stuff in feedback string
        if isinstance(submitted_answer, str):
            contains_bad_chars = all(x in submitted_answer for x in ("<", ">"))
            if contains_bad_chars and submitted_answer in feedback_content:
                raise ValueError(
                    f"Unescaped student input should not be present in the feedback for {question_name}."
                )

        data["partial_scores"][question_name]["feedback"] = feedback_content

        if not feedback_field_name:
            feedback_field_name = question_name

        data["feedback"][feedback_field_name] = feedback_content
