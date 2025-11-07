from typing import Any, Dict

import prairielearn as pl
import theorielearn.thompson.server_base as server_base
from automata.fa.nfa import NFA


def get_thompson_counter1_nfa() -> NFA:
    states = {"a", "b", "c", "d", "f", "g"}
    input_symbols = {"0", "1"}

    transitions = {
        "a": {"0": {"c"}, "1": {"b"}},
        "b": {"0": {"c"}},
        "c": {"1": {"d"}},
        "d": {"": {"c"}, "1": {"f"}},
        "f": {"0": {"g"}},
        "g": {"": {"d"}},
    }

    initial_state = "a"
    final_states = {"g"}
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
        "The student's first idea is to merge the start state $e$ of NFA $T$ into the final state $d$ of NFA $S$ "
        "(reference the Intro question to view these NFAs again). "
        "They reason that this way, a string will first be simulated on $S$, then immediately simulated on $T$. "
        "Is this approach correct? If not, give a counterexample."
    )
    data["params"]["regex_string"] = "(10+0)11*10(10)*"

    server_base.generate(data)


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data, get_thompson_counter1_nfa())
