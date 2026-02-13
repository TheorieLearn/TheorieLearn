"""Functions for error checking in converting JSON to FSMs"""

import copy
from dataclasses import dataclass
from enum import Enum
from typing import Any, TypedDict, TypeVar

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from pyparsing import deque

FSMRawJsonStateT = str
FSMRawTransitionT = dict[FSMRawJsonStateT, dict[str, list[FSMRawJsonStateT]]]

ErrorStatesT = set[str] | None

StartTupleT = tuple[None, None, str]
TransitionTupleT = tuple[str, str, str]
MissingTransitionTupleT = tuple[str, str, None]

ErrorTransitionsT = (
    set[StartTupleT] | set[TransitionTupleT] | set[MissingTransitionTupleT] | None
)


class FSMRawJsonDict(TypedDict):
    input_symbols: list[str]
    states: list[FSMRawJsonStateT]
    transitions: FSMRawTransitionT
    initial_state: list[FSMRawJsonStateT]
    final_states: list[FSMRawJsonStateT]
    epsilon_symbol: str


DFAStateT = Any
DFAPathT = dict[str, DFAStateT]
DFATransitionsT = dict[DFAStateT, DFAPathT]


class DFAJsonDict(TypedDict):
    """A class with type signatures for the dfa json dict"""

    states: list[DFAStateT]
    input_symbols: list[str]
    transitions: DFATransitionsT
    initial_state: DFAStateT
    final_states: list[DFAStateT]


NFAStateT = Any
NFAPathT = dict[str, set[NFAStateT]]
NFATransitionsT = dict[NFAStateT, NFAPathT]
NFA_INITIAL_STATE_NAME = ""


class NFAJsonDict(TypedDict):
    """A class with type signatures for the nfa json dict"""

    states: list[NFAStateT]
    input_symbols: list[str]
    transitions: dict[NFAStateT, dict[str, list[NFAStateT]]]
    initial_state: NFAStateT
    final_states: list[NFAStateT]


class FSMType(Enum):
    DFA = 1
    NFA = 2


@dataclass
class JsonValidationError(Exception):
    """An exception raised for issues in Json validation."""

    states: ErrorStatesT
    transitions: ErrorTransitionsT
    message: str


def convert_states_for_json(
    states_list: list[FSMRawJsonStateT],
    duplicate_message: str = "Duplicate state names:",
) -> list[FSMRawJsonStateT]:
    """
    Check for duplicate states.
    """
    states = set()
    duplicated_names = set()
    for state in states_list:
        if state == "":
            raise JsonValidationError({state}, None, "Some states are missing a name.")
        if state in states:
            duplicated_names.add(state)
        else:
            states.add(state)

    if duplicated_names:
        raise JsonValidationError(duplicated_names, None, duplicate_message)

    return list(states)


def convert_initial_state_for_json(
    initial_state: list[FSMRawJsonStateT],
    *,
    is_nfa: bool,
) -> list[FSMRawJsonStateT]:
    """
    Check there is only one initial state unless nfa
    """
    if len(initial_state) == 0:
        raise JsonValidationError(None, None, "Your FSM is missing a start state.")
    if len(initial_state) > 1 and not is_nfa:
        transitions = {(None, None, state) for state in initial_state}
        raise JsonValidationError(
            set(initial_state), transitions, "Multiple states marked as start states:"
        )
    convert_states_for_json(
        initial_state, "State names with multiple start links:"
    )  # checks for duplicates

    return initial_state


def compress_to_one_start_state(
    student_initial_states: list[FSMRawJsonStateT],
    states: list[FSMRawJsonStateT],
    transitions: FSMRawTransitionT,
) -> FSMRawJsonStateT:
    """
    Compress down to only one initial state through epsilon transitions
    """
    student_initial_states = list(set(student_initial_states))
    if len(student_initial_states) == 1:
        return student_initial_states[0]

    initial_state = NFA_INITIAL_STATE_NAME
    transitions[initial_state] = {"": student_initial_states}
    states.append(initial_state)
    return initial_state


def check_final_states_for_json(final_states: list[FSMRawJsonStateT]) -> None:
    """
    Check that final states are nonempty.
    """
    if len(final_states) == 0:
        raise JsonValidationError(
            None, None, "You must have at least one accepting state."
        )


def check_transitions_invalid_characters_for_json(
    transitions: FSMRawTransitionT, input_symbols: set[str]
) -> None:
    """
    Check for transitions on invalid characters.
    """
    invalid_transitions = set()
    for start_state, transition in transitions.items():
        for char, end_states in transition.items():
            for end_state in end_states:
                if char not in input_symbols:
                    invalid_transitions.add((start_state, char, end_state))

    if invalid_transitions:
        raise JsonValidationError(
            None, invalid_transitions, "Transitions on invalid characters:"
        )


def check_transitions_missed_characters_for_json(
    transitions: FSMRawTransitionT,
    input_symbols: set[str],
    dump_state_tuple: tuple[FSMRawJsonStateT, list[FSMRawJsonStateT]] | None,
    epsilon_symbol: str | None,
) -> None:
    """
    Check that transitioning on characters is never missed. If there is an
    included dump state, then instead add transitions to the dump state.
    """
    missing_transitions: set[tuple[Any, str]] = set()
    for start_state, transition in transitions.items():
        output_chars = set(transition.keys())
        missing_chars = input_symbols.difference(output_chars)

        # Epsilon symbol is never needed
        if epsilon_symbol:
            missing_chars.discard(epsilon_symbol)

        if missing_chars:
            missing_transitions.update(
                (start_state, missing_char) for missing_char in missing_chars
            )

    if missing_transitions:
        if dump_state_tuple is None:
            # If no dump state, then raise an exception based on the missing transitions
            missed_states = {state for state, _ in missing_transitions}

            missing_transitions_display = {
                (state, char, None) for state, char in missing_transitions
            }

            raise JsonValidationError(
                missed_states,
                missing_transitions_display,
                "States missing outgoing transitions:",
            )

        dump_state, states = dump_state_tuple
        # If dump state allowed, add it to the DFA
        states.append(dump_state)

        # If a dump state is marked, then make missing transitions go there
        for start_state, char in missing_transitions:
            transitions[start_state][char] = [dump_state]

        # Then, make the dump state transition nowhere
        transitions[dump_state] = {char: [dump_state] for char in input_symbols}


def check_transitions_duplicate_characters_for_json(
    transitions: FSMRawTransitionT,
) -> None:
    """
    Check that there are no character duplicate transitions. Only needed for DFAs.
    """
    duplicate_transitions: set[tuple[Any, str, Any]] = set()
    for start_state, transition in transitions.items():
        for char, end_states in transition.items():
            if len(end_states) > 1:
                duplicate_transitions.update(
                    (start_state, char, end_state) for end_state in end_states
                )

    if duplicate_transitions:
        raise JsonValidationError(
            None,
            duplicate_transitions,
            "Multiple transitions on the same character coming out of some states:",
        )


def check_transitions_redundant_for_json(transitions: FSMRawTransitionT) -> None:
    """
    Check that there are no identical transitions. Only needed for NFAs. This
    is a less stringent check than check_transitions_duplicate_characters_for_json
    """
    transition_set = set()
    redundant_transitions = set()
    for start_state, transition in transitions.items():
        for char, end_states in transition.items():
            for end_state in end_states:
                transition_tuple = (start_state, char, end_state)

                if transition_tuple in transition_set:
                    redundant_transitions.add(transition_tuple)

                else:
                    transition_set.add(transition_tuple)

    if redundant_transitions:
        raise JsonValidationError(
            None, redundant_transitions, "Identical transitions present:"
        )


def get_reachable_nodes(fa: DFA | NFA) -> set[Any]:
    next_deque: deque[Any] = deque()
    seen: set[Any] = {fa.initial_state}

    next_deque.append(fa.initial_state)

    while next_deque:
        state = next_deque.popleft()

        for next_state in fa.transitions[state].values():
            neighbors: list[Any] = []
            if isinstance(fa, NFA):
                neighbors.extend(next_state)
            else:
                neighbors.append(next_state)

            for next_node in neighbors:
                if next_node in seen:
                    continue

                seen.add(next_node)
                next_deque.append(next_node)

    return seen


def check_for_unreachable_states(fa: DFA | NFA, dump_state_name: str | None) -> None:
    unreachable_states = set(fa.states) - get_reachable_nodes(fa)

    if dump_state_name is not None:
        unreachable_states.discard(dump_state_name)

    if len(unreachable_states) > 0:
        raise JsonValidationError(
            unreachable_states, None, "Unreachable states present:"
        )


def dfa_convert_json(dfa_dict: FSMRawJsonDict, *, dump_state: bool) -> DFAJsonDict:
    """
    Convert raw json dict for serialization as a DFA. Raise an exception if
    the input JSON defines an invalid DFA.
    """
    # Load inital alphabet
    input_symbols_set = list_as_set(dfa_dict["input_symbols"])

    states = convert_states_for_json(dfa_dict["states"])

    initial_state = convert_initial_state_for_json(
        dfa_dict["initial_state"], is_nfa=False
    )[0]

    # Finally, the transition dictionary is one-to-one with the automata constructor.
    transitions = copy.deepcopy(dfa_dict["transitions"])
    check_transitions_invalid_characters_for_json(transitions, input_symbols_set)
    check_transitions_duplicate_characters_for_json(transitions)

    dump_state_name = None

    if dump_state:
        # If dump state is marked, add it to the states set and then do the transition check
        dump_state_name = "dump"

        while dump_state_name in states:
            dump_state_name += "_"

        # Make sure dump state is a string, otherwise causes weird issues
        check_transitions_missed_characters_for_json(
            transitions, input_symbols_set, (dump_state_name, states), None
        )

    else:
        # If dump state is not marked, check as normal
        check_transitions_missed_characters_for_json(
            transitions, input_symbols_set, None, None
        )

    transformed_transitions = {
        start_state: {char: end_states[0] for char, end_states in transition.items()}
        for start_state, transition in transitions.items()
    }

    input_symbols = list(input_symbols_set)

    final_states = dfa_dict["final_states"]
    check_final_states_for_json(final_states)

    dfa_json_dict: DFAJsonDict = {
        "states": states,
        "input_symbols": input_symbols,
        "transitions": transformed_transitions,
        "initial_state": initial_state,
        "final_states": final_states,
    }

    check_for_unreachable_states(dfa_from_json(dfa_json_dict), dump_state_name)

    return dfa_json_dict


def nfa_convert_json(nfa_dict: FSMRawJsonDict) -> NFAJsonDict:
    """
    Convert raw json dict for serialization as a NFA. Raise an exception if
    the input JSON defines an invalid NFA.
    """
    # Load inital alphabet
    input_symbols_set = list_as_set(nfa_dict["input_symbols"])

    states = convert_states_for_json(nfa_dict["states"])

    student_initial_states = convert_initial_state_for_json(
        nfa_dict["initial_state"], is_nfa=True
    )

    # Finally, the transition dictionary is one-to-one with the automata constructor.
    transitions = copy.deepcopy(nfa_dict["transitions"])
    check_transitions_invalid_characters_for_json(transitions, input_symbols_set)
    check_transitions_redundant_for_json(transitions)

    epsilon_symbol = nfa_dict["epsilon_symbol"]

    # Replace epsilon transitions
    for transition in transitions.values():
        if epsilon_symbol in transition:
            transition[""] = transition.pop(epsilon_symbol)

    input_symbols = list(input_symbols_set)
    input_symbols.remove(epsilon_symbol)

    # Replace multiple start states/links with new initial state with epsilon transitions to all student start states
    initial_state = compress_to_one_start_state(
        student_initial_states, states, transitions
    )

    final_states = nfa_dict["final_states"]
    check_final_states_for_json(final_states)

    nfa_json_dict: NFAJsonDict = {
        "states": states,
        "input_symbols": input_symbols,
        "transitions": transitions,
        "initial_state": initial_state,
        "final_states": final_states,
    }

    check_for_unreachable_states(nfa_from_json(nfa_json_dict), None)

    return nfa_json_dict


T = TypeVar("T")


def list_as_set(elem_list: list[T]) -> set[T]:
    """
    Transforms a list to a set, raising an exception if the input has duplicates.
    """
    elem_set = set(elem_list)

    if len(elem_set) != len(elem_list):
        raise ValueError(f"Input list {elem_list!s} has duplicates.")

    return elem_set


def nfa_from_json(json_nfa: NFAJsonDict) -> NFA:
    states = list_as_set(json_nfa["states"])
    input_symbols = list_as_set(json_nfa["input_symbols"])

    # Check for no duplicate states
    json_transitions = json_nfa["transitions"]
    transitions: NFATransitionsT = {}

    for start_state, transition in json_transitions.items():
        transitions[start_state] = {
            char: list_as_set(end_states) for char, end_states in transition.items()
        }

    initial_state = json_nfa["initial_state"]
    final_states = list_as_set(json_nfa["final_states"])
    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )


def dfa_from_json(json_dfa: DFAJsonDict) -> DFA:
    states = list_as_set(json_dfa["states"])
    input_symbols = list_as_set(json_dfa["input_symbols"])
    transitions = json_dfa["transitions"]
    initial_state = json_dfa["initial_state"]
    final_states = list_as_set(json_dfa["final_states"])
    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
