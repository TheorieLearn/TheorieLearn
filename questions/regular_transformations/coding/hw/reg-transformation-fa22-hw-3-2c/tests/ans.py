from automata.fa.nfa import NFA


def transform(M):
    states = {(q, r) for q in M.states for r in ["before", "mid", "after"]}

    input_symbols = {"0", "1"}
    initial_state = (M.initial_state, "before")
    final_states = {(q, "after") for q in M.final_states}

    transitions = {q: {} for q in states}
    for state in M.states:
        transitions[(state, "before")]["1"] = {
            (M.transitions[state]["1"], "before"),
            (state, "mid"),
        }
        transitions[(state, "before")]["0"] = {(M.transitions[state]["0"], "before")}
        transitions[(state, "mid")][""] = {(M.transitions[state]["1"], "after")}

        for symbol in input_symbols:
            transitions[(state, "mid")][symbol] = {
                (M.transitions[state][symbol], "mid")
            }
            transitions[(state, "after")][symbol] = {
                (M.transitions[state][symbol], "after")
            }

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
