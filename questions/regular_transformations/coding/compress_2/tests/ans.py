from automata.fa.dfa import DFA
from automata.fa.nfa import NFA


def transform(M: DFA) -> NFA:
    states = {(q, a) for q in M.states for a in ["any", "next1"]}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    for q in M.states:
        transitions[(q, "any")]["0"] = [
            (M.transitions[M.transitions[q]["0"]]["0"], "any"),
            (M.transitions[q]["0"], "next1"),
        ]
        transitions[(q, "next1")]["0"] = []
        transitions[(q, "any")]["1"] = [(M.transitions[q]["1"], "any")]
        transitions[(q, "next1")]["1"] = [(M.transitions[q]["1"], "any")]

    initial_state = (M.initial_state, "any")
    final_states = {(q, a) for q in M.final_states for a in ["any", "next1"]}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
