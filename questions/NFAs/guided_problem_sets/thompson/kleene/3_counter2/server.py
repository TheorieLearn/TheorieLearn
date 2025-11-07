from typing import Any, Dict

import prairielearn as pl
import theorielearn.thompson.server_base as server_base
from automata.fa.nfa import NFA


def get_thompson_counter2_nfa() -> NFA:
    states = {"a", "b", "c", "d", "e"}
    input_symbols = {"0", "1"}

    transitions = {
        "a": {"0": {"b"}},
        "b": {"0": {"d"}, "1": {"c"}},
        "c": {"1": {"a"}},
        "d": {"0": {"e"}},
        "e": {"": {"a"}},
    }

    initial_state = "a"
    final_states = {"e", "a"}
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
        "We now know that the previous example is incorrect because it does not accept the empty string. "
        "To solve this issue, the student decides to make the start state $a$ also an accepting state. "
        "Is this approach correct? If not, give a counterexample."
    )
    data["params"]["regex_string"] = "((011)*000)*"

    server_base.generate(data)


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data, get_thompson_counter2_nfa())
