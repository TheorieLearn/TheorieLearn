from automata.fa.dfa import DFA


def transform(M):
    states = {(q, a) for q in M.states for a in [0, 1, 2]}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    for q in M.states:
        for a in input_symbols:
            for i in [0, 1]:
                transitions[(q, i)][a] = (q, i + 1)

            transitions[(q, 2)][a] = (M.transitions[q][a], 0)

    initial_state = (M.initial_state, 0)
    final_states = {(q, a) for q in M.final_states for a in [0, 1, 2]}

    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
