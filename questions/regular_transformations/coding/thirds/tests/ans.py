from automata.fa.nfa import NFA


def transform(M):
    states = M.states
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    # d(d(d(q,c),b),a)
    # q = q1
    # d(q, c) = q2
    # d(d(q,c),b) = q3
    for q1 in M.states:
        for a in input_symbols:
            temp_transitions = set()
            for c in input_symbols:
                q2 = M.transitions[q1][c]
                for b in input_symbols:
                    q3 = M.transitions[q2][b]
                    temp_transitions.add(M.transitions[q3][a])

            transitions[q1][a] = list(temp_transitions)

    initial_state = M.initial_state
    final_states = M.final_states

    for q in M.states:
        for a in input_symbols:
            q2 = M.transitions[q][a]
            possible_final = {q2}
            for b in input_symbols:
                possible_final |= {M.transitions[q2][b]}
                if len(possible_final & M.final_states) != 0:
                    final_states |= possible_final

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
