from typing import Any, Dict

import prairielearn as pl
import theorielearn.thompson.server_base as server_base
from automata.fa.nfa import NFA


def get_thompson_kleene_nfa() -> NFA:
    states = {"s", "f", "a", "b", "c", "d", "e"}
    input_symbols = {"0", "1"}

    transitions = {
        "s": {
            "": {"a", "f"},
        },
        "a": {"0": {"b"}},
        "b": {"0": {"d"}, "1": {"c"}},
        "c": {"1": {"a"}},
        "d": {"0": {"e"}},
        "e": {"": {"f"}},
        "f": {"": {"s"}},
    }

    initial_state = "s"
    final_states = {"f"}
    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )


def generate(data: Dict[str, Any]) -> None:
    data["params"]["nfa"] = get_thompson_kleene_nfa().show_diagram().string()
    data["params"]["description"] = (
        "At this point the student understands that simply accepting the start state is problematic; "
        "it would lead to incorrectly accepted inputs if there are any paths leading back to the start state (other than the $\\varepsilon$-transition they added). "
        "The student adds a new start state $s$ with an $\\varepsilon$-transition to $a$ as well as "
        "a final state $f$ in accordance to Thompson's algorithm. Is this approach correct? If not, give a counterexample."
    )
    data["params"]["regex_string"] = "((011)*000)*"

    server_base.generate(data)


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data, get_thompson_kleene_nfa())
