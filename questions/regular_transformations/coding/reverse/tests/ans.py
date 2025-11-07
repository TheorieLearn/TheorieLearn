from automata.fa.nfa import NFA


def transform(M):
    states = M.states | {"START"}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    transitions["START"][""] = M.final_states

    for q in M.states:
        for a in input_symbols:
            transitions[q][a] = {r for r in M.states if M.transitions[r][a] == q}

    initial_state = "START"
    final_states = {M.initial_state}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
