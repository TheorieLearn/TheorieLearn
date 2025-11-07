from automata.fa.nfa import NFA


def transform(M):
    states = {
        (q, label) for q in M.states for label in ["before", "between1and0", "after"]
    }
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    for q in M.states:
        transitions[(q, "before")]["0"] = {(M.transitions[q]["0"], "before")}
        transitions[(q, "before")]["1"] = {
            (M.transitions[q]["1"], "before"),
            (q, "between1and0"),
        }

        transitions[(q, "between1and0")]["0"] = {(q, "after")}

        for a in input_symbols:
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
