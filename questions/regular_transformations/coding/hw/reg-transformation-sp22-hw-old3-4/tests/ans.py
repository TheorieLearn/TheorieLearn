from automata.fa.nfa import NFA


def transform(M):
    states = (
        {(q, "before") for q in M.states}
        | {(q, "middle") for q in M.states}
        | {(q, "after") for q in M.states}
    )
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}

    def flip(a):
        return "0" if a == "1" else "1"

    for q in M.states:
        transitions[(q, "before")][""] = {(q, "middle")}
        transitions[(q, "middle")][""] = {(q, "after")}
        for a in input_symbols:
            transitions[(q, "before")][a] = {(M.transitions[q][a], "before")}
            transitions[(q, "middle")][a] = {(M.transitions[q][flip(a)], "middle")}
            transitions[(q, "after")][a] = {(M.transitions[q][a], "after")}

    initial_state = (M.initial_state, "before")
    final_states = {(q, "after") for q in M.final_states}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
