from typing import Any, TypedDict, TypeVar

from automata.fa.dfa import DFA

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


T = TypeVar("T")


def list_as_set(elem_list: list[T]) -> set[T]:
    """
    Transforms a list to a set, raising an exception if the input has duplicates.
    """
    elem_set = set(elem_list)

    if len(elem_set) != len(elem_list):
        raise ValueError(f"Input list {elem_list!s} has duplicates.")

    return elem_set


def dfa_dump_json(dfa: DFA) -> DFAJsonDict:
    state_map = {state: str(i) for i, state in enumerate(dfa.states)}
    json_states = sorted(state_map[state] for state in dfa.states)
    json_input_symbols = sorted(dfa.input_symbols)

    json_transitions = {
        state_map[start_state]: {
            char: state_map[end_state] for char, end_state in transition.items()
        }
        for start_state, transition in dfa.transitions.items()
    }

    json_initial_state = state_map[dfa.initial_state]
    json_final_states = sorted(state_map[state] for state in dfa.final_states)

    return {
        "states": json_states,
        "input_symbols": json_input_symbols,
        "transitions": json_transitions,
        "initial_state": json_initial_state,
        "final_states": json_final_states,
    }


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
