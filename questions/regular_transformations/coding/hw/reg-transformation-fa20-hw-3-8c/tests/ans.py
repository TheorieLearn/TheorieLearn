from automata.fa.nfa import NFA


def transform(M):
    states = {(qx, qy) for qx in M.states for qy in M.states}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}

    for qx in M.states:
        for qy in M.states:
            transitions[(qx, qy)]["0"] = {
                (M.transitions[qx]["1"], M.transitions[qy]["1"]),
                (M.transitions[qx]["0"], M.transitions[qy]["0"]),
            }
            transitions[(qx, qy)]["1"] = {
                (M.transitions[qx]["0"], M.transitions[qy]["1"]),
                (M.transitions[qx]["1"], M.transitions[qy]["0"]),
            }

    initial_state = (M.initial_state, M.initial_state)
    final_states = {(qx, qy) for qx in M.final_states for qy in M.final_states}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
