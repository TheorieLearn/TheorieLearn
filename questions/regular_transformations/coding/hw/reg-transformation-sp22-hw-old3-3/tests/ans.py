from itertools import product

from automata.fa.nfa import NFA


def transform(M):
    states = {tuple(state) for state in product(M.states, repeat=3)} | {"s'"}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    transitions["s'"][""] = {(M.initial_state, h, h) for h in M.states}

    for state in states:
        if state != "s'":
            for symbol in input_symbols:
                p = state[0]
                h = state[1]
                q = state[2]
                transitions[state][symbol] = {
                    (M.transitions[p][symbol], h, M.transitions[q][symbol])
                }

    initial_state = "s'"
    final_states = {(h, h, q) for q in M.final_states for h in M.states}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
