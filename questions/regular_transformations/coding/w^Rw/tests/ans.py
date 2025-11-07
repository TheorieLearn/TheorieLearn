from automata.fa.nfa import NFA


def transform(M):
    states = {(qi, qj) for qi in M.states for qj in M.states} | {"START"}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    transitions["START"][""] = {(q, q) for q in M.states}

    for qi in M.states:
        for qj in M.states:
            for a in input_symbols:
                transitions[(qi, qj)][a] = {
                    (M.transitions[qi][a], r)
                    for r in M.states
                    if M.transitions[r][a] == qj
                }

    initial_state = "START"
    final_states = {(qj, M.initial_state) for qj in M.final_states}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
