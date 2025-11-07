import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "INSERT01"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$\mathsf{INSERT01}(L) := \{ x01y \mid xy \in L \}.$$
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it will feed the characters to a simulation of $M$. However, $M'$ will *non-deterministically* choose a single `01` substring to omit from the simulation. Keeping this intuition in mind, we will now make the description more formal.

Every state $q$ in the DFA $M$ will correspond to three states in $M'$, as described below:

- The state $(q, \varepsilon)$ means that the simulation of $M$ is in state $q$ and $M'$ has not read any part of the inserted `01`.
- The state $(q, 0)$ means that the simulation of $M$ is in state $q$ and $M'$ has just read the `0` from the inserted `01`.
- The state $(q, 01)$ means that the simulation of $M$ is in state $q$ and $M'$ has already read and omitted the inserted `01`.
"""

BEFORE = "ε"
BETWEEN = "0"
AFTER = "01"
STATE_LABELS = [BEFORE, BETWEEN, AFTER]


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if it has no self-loops.
    This ensures students understand that characters are being omitted from the simulation of M.
    When there are self-loops, simulating vs. not simulating a character could have the same result.
    """

    return all(
        M.transitions[q][a] != q for (q, a) in product(M.states, M.input_symbols)
    )


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    states = set(product(M.states, STATE_LABELS))

    transitions: NFATransitionsT = {q_prime: dict() for q_prime in states}
    for q in M.states:
        transitions[(q, BEFORE)]["0"] = {(q, BETWEEN), (M.transitions[q]["0"], BEFORE)}
        transitions[(q, BEFORE)]["1"] = {(M.transitions[q]["1"], BEFORE)}

        transitions[(q, BETWEEN)]["0"] = set()
        transitions[(q, BETWEEN)]["1"] = {(q, AFTER)}

        for a in M.input_symbols:
            transitions[(q, AFTER)][a] = {(M.transitions[q][a], AFTER)}

    initial_state = (M.initial_state, BEFORE)

    final_states = set(product(M.final_states, {AFTER}))

    return NFA(
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
        ((random.choice(list(M.states)), label), a)
        for label in STATE_LABELS
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
