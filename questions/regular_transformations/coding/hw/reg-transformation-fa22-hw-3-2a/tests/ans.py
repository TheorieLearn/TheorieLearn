from automata.fa.nfa import NFA


def transform(M):
    states = M.states | {"accept"}

    input_symbols = {"0", "1"}
    initial_state = M.initial_state
    final_states = {"accept"}

    transitions = {q: {} for q in states}
    transitions[M.initial_state][""] = {
        M.transitions[M.initial_state][symbol] for symbol in input_symbols
    }
    for state in M.states:
        if state != M.initial_state and state not in M.final_states:
            for symbol in input_symbols:
                transitions[state][symbol] = {M.transitions[state][symbol]}
    for state in M.final_states:
        transitions[state]["0"] = {"accept", M.transitions[state]["0"]}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
