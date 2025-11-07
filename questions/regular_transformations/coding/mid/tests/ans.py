from automata.fa.nfa import NFA


def transform(M):
    states = {
        (q, label)
        for q in M.states
        for label in ["simulatingX", "readingW", "simulatingY"]
    }
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    for q in M.states:
        transitions[(q, "simulatingX")][""] = {
            (M.transitions[q][a], "simulatingX") for a in input_symbols
        } | {(q, "readingW")}

        for a in input_symbols:
            transitions[(q, "readingW")][a] = {(M.transitions[q][a], "readingW")}
        transitions[(q, "readingW")][""] = {(q, "simulatingY")}

        transitions[(q, "simulatingY")][""] = {
            (M.transitions[q][a], "simulatingY") for a in input_symbols
        }

    initial_state = (M.initial_state, "simulatingX")
    final_states = {(q, "simulatingY") for q in M.final_states}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
