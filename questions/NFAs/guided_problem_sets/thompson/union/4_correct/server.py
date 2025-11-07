from typing import Any, Dict

import prairielearn as pl
import theorielearn.thompson.server_base as server_base
from automata.fa.nfa import NFA, NFATransitionsT


def get_thompson_union_nfa() -> NFA:
    states = {"s", "a", "b", "c", "d", "e", "f", "g", "h"}
    input_symbols = {"0", "1"}

    transitions: NFATransitionsT = {
        "s": {
            "": {"a", "d"},
        },
        "a": {"0": {"b"}, "": {"h"}},
        "b": {"1": {"c"}},
        "c": {"0": {"a"}},
        "d": {"0": {"e"}},
        "e": {"1": {"f"}},
        "f": {"0": {"g"}},
        "g": {"0": {"g"}, "": {"h"}},
        "h": {},
    }

    initial_state = "s"
    final_states = {"h"}
    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )


def generate(data: Dict[str, Any]) -> None:
    data["params"]["nfa"] = get_thompson_union_nfa().show_diagram().string()
    data["params"]["description"] = (
        "At this point the student understands that simply merging the start states of $S$ and $T$ would lead "
        "to incorrectly accepted strings if any path exists between the two NFAs. "
        "The student adds a new start state $s$ with $\\varepsilon$-transitions to the start states of $S$ and $T$. "
        "They also add a final state $h$ to gather the final states of $S$ and $T$. "
        "Is this approach correct? If not, give a counterexample."
    )
    data["params"]["regex_string"] = "(010)*+0100*"

    server_base.generate(data)


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data, get_thompson_union_nfa())
