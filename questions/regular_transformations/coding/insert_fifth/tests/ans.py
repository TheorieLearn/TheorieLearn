from automata.fa.dfa import DFA


def transform(M):
    states = {(q, i, "before") for q in M.states for i in range(5)} | {
        (q, "after") for q in M.states
    }

    transitions = {q: {} for q in states}

    for q in M.states:
        for c in ["0", "1"]:
            for i in range(4):
                transitions[(q, i, "before")][c] = (
                    M.transitions[q][c],
                    i + 1,
                    "before",
                )

            transitions[(q, 4, "before")][c] = (q, "after")
            transitions[(q, "after")][c] = (M.transitions[q][c], "after")

    initial_state = (M.initial_state, 0, "before")
    final_states = {(q, "after") for q in M.final_states}

    return DFA(
        states=states,
        input_symbols={"0", "1"},
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
