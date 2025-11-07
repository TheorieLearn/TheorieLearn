from automata.fa.nfa import NFA


def transform(M):
    states = M.states
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    for q in M.states:
        transitions[q]["0"] = {M.transitions[q]["0"]}
        transitions[q]["1"] = {}
        transitions[q][""] = {M.transitions[q]["1"]}

    initial_state = M.initial_state
    final_states = M.final_states

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
