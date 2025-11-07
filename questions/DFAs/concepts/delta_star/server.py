import random
from itertools import product
from random import randint, shuffle

import prairielearn as pl
from automata.fa.dfa import DFA


def generate_random_dfa(lower: int, upper: int) -> DFA:
    n = randint(lower, upper)
    input_symbols = {"0", "1"}
    states = set(range(n))
    random_state_ordering = list(states)
    shuffle(random_state_ordering)

    transitions: dict[int, dict[str, int]] = {i: {} for i in states}
    initial_state = random_state_ordering[0]

    for i in range(n - 1):
        symbol = str(randint(0, 1))
        origin_state, destination_state = (
            random_state_ordering[i],
            random_state_ordering[i + 1],
        )
        transitions[origin_state][symbol] = destination_state

    for transition, symbol in product(transitions.values(), input_symbols):
        if symbol not in transition:
            transition[symbol] = randint(0, n - 1)

    final_states = {state for state in states if randint(0, 1)}
    if len(final_states) == 0:
        final_states.add(randint(0, n - 1))
    if len(final_states) == n:
        final_states.remove(randint(0, n - 1))

    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )


def generate(data: pl.QuestionData) -> None:
    dfa = generate_random_dfa(3, 7)
    data["params"]["dfa"] = str(dfa.show_diagram())

    is_empty_input = random.choice(range(5)) == 0
    rand_state = random.choice(list(dfa.states))

    if is_empty_input:
        input_str = r"\varepsilon"
        data["correct_answers"]["ans"] = str(rand_state)
    else:
        rand_len = random.choice(range(1, 8))
        input_str = "".join(random.choices(["0", "1"], k=rand_len))
        temp_dfa = DFA(
            states=dfa.states,
            input_symbols=dfa.input_symbols,
            transitions=dfa.transitions,
            initial_state=rand_state,
            final_states=dfa.final_states,
            allow_partial=dfa.allow_partial,
        )
        data["correct_answers"]["ans"] = str(
            list(temp_dfa.read_input_stepwise(input_str, ignore_rejection=True))[-1]
        )

    data["params"]["input"] = input_str
    data["params"]["start_state"] = rand_state
