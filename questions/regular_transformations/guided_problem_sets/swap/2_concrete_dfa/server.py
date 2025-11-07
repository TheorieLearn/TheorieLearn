import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import dfa_read_input_from_state, generate_random_dfa
from automata.fa.dfa import DFA, DFATransitionsT

EPSILON = "ε"

TRANSFORMATION_NAME = "SWAP"

TRANSFORMATION_DEFINITION = r"""
$\mathsf{SWAP}(L) := \{\mathsf{swap}(w) \mid w \in L \}$, where $\mathsf{swap}(w)$ is defined recursively as

$$
\mathsf{swap}(w) := \begin{cases}
    w &\text{if } |w| \leq 1\\
    ba \bullet \mathsf{swap}(x) &\text{if } w = ab \bullet x \text{ for some } a, b \in \Sigma \text{ and } x \in \Sigma^*
\end{cases}
$$
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, $M'$ will read the string in two character chunks, swap the two characters, and simulate $M$ on the swapped pair of characters. This means that when $M'$ reads an odd-indexed character; it cannot immediately simulate $M$ on that character. Instead, it must remember that odd-indexed character until it reads the next (even-indexed) character, so that it can swap those two characters and feed them to the simulation of $M$. Keeping this intuition in mind, we will now make the description more formal.

Every state $q$ in the DFA $M$ will correspond to $|\Sigma| + 1$ states in $M'$, as described below:

- The state $(q, \varepsilon)$ means that the simulation of $M$ is in state $q$, and the number of characters read so far is even.
- For each character $a \in \Sigma$, the state $(q, a)$ means that the simulation of $M$ is in state $q$, the number of characters read so far is odd, and the last character read was $a$. (In this state, the last character $a$ has not yet been fed to the simulation of $M$)
"""


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if:
    - (q, a) is in A' for at least one q not in A, and
    - (q, a) is not in A' for at least one q in A
    - reading 01 never does the same thing as reading 10

    This choice of DFA ensures that students understand that there's no correlation between
    whether q is in A and whether (q, a) is in A'.
    """

    nonaccepting_states = M.states - M.final_states

    return (
        any(
            M.transitions[q][a] in M.final_states
            for (q, a) in product(nonaccepting_states, M.input_symbols)
        )
        and any(
            M.transitions[q][a] in nonaccepting_states
            for (q, a) in product(M.final_states, M.input_symbols)
        )
        and all(
            dfa_read_input_from_state(M, q, "01") != dfa_read_input_from_state(M, q, "10")
            for q in M.states
        )
    )


def construct_M_prime(M: DFA) -> DFA:
    states = set(product(M.states, {EPSILON} | M.input_symbols))

    transitions: DFATransitionsT = {q_prime: dict() for q_prime in states}
    for q in M.states:
        for a in M.input_symbols:
            transitions[(q, EPSILON)][a] = (q, a)

            for b in M.input_symbols:
                transitions[(q, b)][a] = (
                    M.transitions[M.transitions[q][a]][b],
                    EPSILON,
                )

    initial_state = (M.initial_state, EPSILON)

    final_states = {(q, EPSILON) for q in M.final_states} | {
        (q, a)
        for (q, a) in product(M.states, M.input_symbols)
        if M.transitions[q][a] in M.final_states
    }

    return DFA(
        states=states,
        input_symbols=M.input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )


def generate(data: Dict[str, Any]) -> None:
    M = generate_random_dfa(3, 3)
    while not should_use_dfa(M):
        M = generate_random_dfa(3, 3)

    transitions_to_ask = [
        ((random.choice(list(M.states)), stored_char), a)
        for stored_char in {EPSILON} | M.input_symbols
        for a in M.input_symbols
    ]

    server_base.generate(
        data,
        TRANSFORMATION_NAME,
        TRANSFORMATION_DEFINITION,
        DESCRIPTION_OF_STATES,
        M,
        construct_M_prime(M),
        transitions_to_ask,
    )


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data)
