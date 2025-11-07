from typing import Any, Dict

import prairielearn as pl
import theorielearn.thompson.server_base as server_base
from automata.fa.nfa import NFA, NFATransitionsT


def get_thompson_counter2_nfa() -> NFA:
    states = {"a", "b", "c", "e", "f", "g", "h"}
    input_symbols = {"0", "1"}

    transitions: NFATransitionsT = {
        "a": {"0": {"b", "e"}, "": {"h"}},
        "b": {"1": {"c"}},
        "c": {"0": {"a"}},
        "e": {"1": {"f"}},
        "f": {"0": {"g"}},
        "g": {"0": {"g"}, "": {"h"}},
        "h": {},
    }

    initial_state = "a"
    final_states = {"h"}
    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )


def generate(data: Dict[str, Any]) -> None:
    data["params"]["nfa"] = get_thompson_counter2_nfa().show_diagram().string()
    data["params"]["description"] = (
        "The student realizes their first approach was incorrect, but they cannot pinpoint the exact reason. "
        '"Perhaps it was because the start state was an accepting state?" They add a new end state $h$ '
        "to gather the accepting states of $S$ and $T$. Is this new approach correct? If not, give a counterexample."
    )
    data["params"]["regex_string"] = "(010)*+0100*"

    server_base.generate(data)


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data, get_thompson_counter2_nfa())
