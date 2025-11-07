from automata.fa.nfa import NFA


def transform(M):
    states = {(qi, qj) for qi in M.states for qj in M.states} | {"START"}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    transitions["START"][""] = {(M.initial_state, qj) for qj in M.final_states}

    for qi in M.states:
        for qj in M.states:
            for a in input_symbols:
                transitions[(qi, qj)][a] = {
                    (M.transitions[qi][a], r)
                    for r in M.states
                    if M.transitions[r][a] == qj
                }

    initial_state = "START"
    final_states = {(q, q) for q in M.states}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
