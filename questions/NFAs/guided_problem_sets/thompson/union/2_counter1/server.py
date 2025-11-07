from typing import Any, Dict

import prairielearn as pl
import theorielearn.thompson.server_base as server_base
from automata.fa.nfa import NFA


def get_thompson_counter1_nfa() -> NFA:
    states = {"a", "b", "c", "e", "f", "g"}
    input_symbols = {"0", "1"}

    transitions = {
        "a": {"0": {"b", "e"}},
        "b": {"1": {"c"}},
        "c": {"0": {"a"}},
        "e": {"1": {"f"}},
        "f": {"0": {"g"}},
        "g": {"0": {"g"}},
    }

    initial_state = "a"
    final_states = {"a", "g"}
    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )


def generate(data: Dict[str, Any]) -> None:
    data["params"]["nfa"] = get_thompson_counter1_nfa().show_diagram().string()
    data["params"]["description"] = (
        "The student's first idea is to merge the start state $d$ of NFA $T$ into the start state $a$ of NFAs $S$ "
        "(reference the Intro question to view these NFAs again). They reason that as long as they preserve the outgoing transitions, "
        "the new NFA should correctly simulate reading on both machines for the language union. Is this approach correct? If not, give a counterexample."
    )
    data["params"]["regex_string"] = "(010)*+0100*"

    server_base.generate(data)


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data, get_thompson_counter1_nfa())
