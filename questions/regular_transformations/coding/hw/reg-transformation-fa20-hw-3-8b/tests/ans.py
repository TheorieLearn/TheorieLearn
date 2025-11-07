from automata.fa.nfa import NFA


def transform(M):
    states = {(q, "before") for q in M.states} | {(q, "after") for q in M.states}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}

    for q in M.states:
        if q in M.final_states:
            transitions[(q, "before")][""] = {(p, "after") for p in M.final_states}
        for a in input_symbols:
            transitions[(q, "before")][a] = {(M.transitions[q][a], "before")}
            transitions[(q, "after")][a] = {
                (p, "after") for p in M.states if M.transitions[p][a] == q
            }

    initial_state = (M.initial_state, "before")
    final_states = {(M.initial_state, "after")}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
