from typing import Set

from automata.fa.dfa import DFA


def transform(M):
    # find all states that are 2 or more steps away from an accepting state
    reverse_transitions = {q: {} for q in M.states}
    for state in M.states:
        for sym in M.input_symbols:
            end_loc = M.transitions[state][sym]
            if sym not in reverse_transitions[end_loc]:
                reverse_transitions[end_loc][sym] = {state}
            else:
                reverse_transitions[end_loc][sym].add(state)

    def rec_traverse(
        final_states: Set[str], state: str, have_seen: Set[str], depth: int
    ) -> None:
        if state in have_seen:
            return
        if depth >= 2:
            final_states |= {state}
            have_seen.add(state)

        for sym in M.input_symbols:
            if sym in reverse_transitions[state]:
                for n in reverse_transitions[state][sym]:
                    rec_traverse(final_states, n, have_seen, depth + 1)

    fs = set()

    for start_final in M.final_states:
        rec_traverse(fs, start_final, set(), 0)

    # this turns the transitions into the form of an NFA if you wanted to return a NFA instead
    # transitions = {q: {} for q in M.states}
    # for q in M.states:
    #     for sym in M.input_symbols:
    #         transitions[q][sym] = [M.transitions[q][sym]]

    return DFA(
        states=M.states,
        input_symbols=M.input_symbols,
        transitions=M.transitions,
        initial_state=M.initial_state,
        final_states=fs,
    )
