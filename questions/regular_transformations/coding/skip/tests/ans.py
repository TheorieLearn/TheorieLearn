from automata.fa.nfa import NFA


def transform(M):
    states = M.states | {"q_a"}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    # d(d(q,a),b)
    # q = q1
    # d(q, a) = q2
    for q1 in M.states:
        for a in input_symbols:
            temp_transitions = set()
            for b in input_symbols:
                q2 = M.transitions[q1][a]
                temp_transitions.add(M.transitions[q2][b])

            if M.transitions[q1][a] in M.final_states:
                temp_transitions.add("q_a")

            transitions[q1][a] = temp_transitions

    for s in input_symbols:
        transitions["q_a"][s] = []

    initial_state = M.initial_state
    final_states = M.final_states | {"q_a"}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
