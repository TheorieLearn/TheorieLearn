from automata.fa.nfa import NFA


def transform(M):
    states = (
        {(q, "before") for q in M.states}
        | {
            (q, a, i, "middle")
            for q in M.states
            for a in M.input_symbols
            for i in range(9)
        }
        | {(q, "after") for q in M.states}
    )
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}

    for q in M.states:
        for a in input_symbols:
            transitions[(q, "before")][a] = {
                (M.transitions[q][a], "before"),
                (q, a, 0, "middle"),
            }
            transitions[(q, "after")][a] = {(M.transitions[q][a], "after")}
            for b in input_symbols:
                for i in range(9):
                    if i <= 7:
                        transitions[(q, a, i, "middle")][b] = {
                            (M.transitions[q][b], a, i + 1, "middle")
                        }
                    transitions[(q, a, i, "middle")][""] = {
                        (M.transitions[q][a], "after")
                    }

    initial_state = (M.initial_state, "before")
    final_states = {(q, "after") for q in M.final_states}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
