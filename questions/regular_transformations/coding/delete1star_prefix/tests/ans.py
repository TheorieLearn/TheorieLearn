from automata.fa.nfa import NFA


def transform(M):
    states = {(q, label) for q in M.states for label in ["inserting1s", "after"]}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    for q in M.states:
        transitions[(q, "inserting1s")][""] = {
            (M.transitions[q]["1"], "inserting1s"),
            (q, "after"),
        }

        for a in input_symbols:
            transitions[(q, "after")][a] = {(M.transitions[q][a], "after")}

    initial_state = (M.initial_state, "inserting1s")
    final_states = {(q, "after") for q in M.final_states}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
