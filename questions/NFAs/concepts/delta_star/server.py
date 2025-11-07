import random

import prairielearn as pl
from automata.base.exceptions import RejectionException
from automata.fa.nfa import NFA
from theorielearn.automata_utils.fa_utils import generate_random_nfa
from theorielearn.shared_utils import grade_question_tokenized


def generate(data: pl.QuestionData) -> None:
    nfa = generate_random_nfa(
        states=6,
        alphabet="01",
        edge_density=0.4,
        epsilon_density=0.3,
        accepting=2,
    )
    data["params"]["nfa"] = str(nfa.show_diagram())

    rand_state = random.choice(list(nfa.states))
    rand_len = random.randint(2, 3)
    input_str = "".join(random.choices(["0", "1"], k=rand_len))

    data["params"]["start_state"] = rand_state
    data["params"]["input"] = input_str

    temp_nfa = NFA(
        states=nfa.states,
        input_symbols=nfa.input_symbols,
        transitions=nfa.transitions,
        initial_state=rand_state,
        final_states=nfa.final_states,
    )
    state_generator = temp_nfa.read_input_stepwise(input_str)
    set_ans_states: set = set()
    try:
        for state_set in state_generator:
            set_ans_states = set(state_set)
    except RejectionException:
        pass

    data["correct_answers"]["ans"] = f"{{{','.join(set_ans_states)}}}"


def grade(data: pl.QuestionData) -> None:
    grade_question_tokenized(data, "ans")
    pl.set_weighted_score_data(data)
