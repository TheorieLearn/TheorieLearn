from automata.fa.dfa import DFA


def transform(M: DFA) -> DFA:
    states = {(q, a) for q in M.states for a in [0, 1]}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    for q in M.states:
        transitions[(q, 0)]["0"] = (M.transitions[q]["0"], 1)
        transitions[(q, 1)]["0"] = (q, 0)
        transitions[(q, 0)]["1"] = (M.transitions[q]["1"], 0)
        transitions[(q, 1)]["1"] = (M.transitions[q]["1"], 0)

    initial_state = (M.initial_state, 0)
    final_states = {(q, a) for q in M.final_states for a in [0, 1]}

    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
