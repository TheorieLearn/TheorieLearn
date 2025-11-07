from automata.fa.nfa import NFA


def transform(M):
    states = {(q, "before") for q in M.states} | {
        (q, i, "after") for q in M.states for i in range(5)
    }
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}

    for q in M.states:
        transitions[(q, "before")][""] = {
            (M.transitions[q][a], 0, "after") for a in input_symbols
        }

        for c in input_symbols:
            transitions[(q, "before")][c] = {(M.transitions[q][c], "before")}

            for i in range(4):
                transitions[(q, i, "after")][c] = {
                    (M.transitions[q][c], i + 1, "after")
                }

    initial_state = (M.initial_state, "before")
    final_states = {(q, 4, "after") for q in M.final_states}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
