from automata.fa.dfa import DFA


def transform(M: DFA) -> DFA:
    # p=0 even parity, p=1 odd parity
    parities = [0, 1]
    currchars = [0, 1, None]
    states = {(q, c, p) for q in M.states for c in currchars for p in parities}
    input_symbols = {"0", "1"}

    transitions = {q: {} for q in states}
    for q in M.states:
        for c in currchars:
            for p in parities:
                for nextchar in input_symbols:
                    nextcharint = int(nextchar)
                    if c == None:
                        transitions[(q, c, p)][nextchar] = (q, nextcharint, 1)
                    elif c == nextcharint:
                        transitions[(q, c, p)][nextchar] = (q, nextcharint, 1 - p)
                    else:
                        transitions[(q, c, p)][nextchar] = (M.transitions[q][str(p)], nextcharint, 1)


    initial_state = (M.initial_state, None, 0)
    final_states = set()
    for q, c, p in states:
        if (c == None and q in M.final_states) or (c != None and M.transitions[q][str(p)] in M.final_states):
            final_states.add((q, c, p))

    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )
