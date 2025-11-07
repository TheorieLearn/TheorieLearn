from automata.fa.dfa import DFA


def transform(M):
    states = {(q, flip) for q in M.states for flip in [True, False]}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    for q in M.states:
        transitions[(q, False)]["0"] = (M.transitions[q]["0"], True)
        transitions[(q, True)]["0"] = (M.transitions[q]["1"], False)
        transitions[(q, False)]["1"] = (M.transitions[q]["1"], True)
        transitions[(q, True)]["1"] = (M.transitions[q]["0"], False)

    initial_state = (M.initial_state, False)
    final_states = {(q, flip) for q in M.final_states for flip in [True, False]}

    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
