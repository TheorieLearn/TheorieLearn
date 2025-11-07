import random
from enum import IntEnum

import theorielearn.shared_utils as su
from automata.fa.dfa import DFA
from theorielearn.automata_utils.fa_utils import generate_random_dfa, generate_dfa_html_description
from typing_extensions import assert_never


class QuestionType(IntEnum):
    BOTH = 0
    AT_LEAST_ONE = 1
    EXACTLY_ONE = 2
    NEITHER = 3


SET_DESCRIPTIONS = {
    QuestionType.BOTH: r"$A = A_1 \times A_2$",
    QuestionType.AT_LEAST_ONE: r"$A = \{(p, q) \space | \space p \in A_1 \space or \space q \in A_2\}$",
    QuestionType.EXACTLY_ONE: r"$A = \{(p, q) \space | \space (p \in A_1 \space and \space q \notin A_2) \space or \space (p \notin A_1 \space and \space q \in A_2)\}$",
    QuestionType.NEITHER: r"$A = \{(p, q) \space | \space p \notin A_1 \space and \space q \notin A_2\}$",
}


def generate(data: su.QuestionData) -> None:
    dfa1 = generate_random_dfa(3, 5)
    dfa2 = generate_random_dfa(3, 5)

    transition_start_1 = random.randint(0, len(dfa1.states) - 1)
    transition_start_2 = random.randint(0, len(dfa2.states) - 1)

    transition_symbol = random.choice(["0", "1"])

    question_type = random.choice(list(QuestionType))

    desc_list = [
        {"description": "both", "correct": "false"},
        {"description": "at least one", "correct": "false"},
        {"description": "exactly one", "correct": "false"},
        {"description": "neither", "correct": "false"},
    ]

    desc_list[int(question_type)]["correct"] = "true"

    new_dfa = None

    if question_type is QuestionType.BOTH:
        new_dfa = dfa1.intersection(dfa2, retain_names=True, minify=False)
    elif question_type is QuestionType.AT_LEAST_ONE:
        new_dfa = dfa1.union(dfa2, retain_names=True, minify=False)
    elif question_type is QuestionType.EXACTLY_ONE:
        new_dfa = dfa1.symmetric_difference(dfa2, retain_names=True, minify=False)
    elif question_type is QuestionType.NEITHER:
        new_dfa = (~dfa1).intersection(~dfa2, retain_names=True, minify=False)
    else:
        assert_never(question_type)

    final_states = list(new_dfa.final_states)
    rejecting_states = list(new_dfa.states - new_dfa.final_states)

    random.shuffle(rejecting_states)
    num_answers = 5
    num_correct_answers = random.randint(
        max(1, num_answers - len(rejecting_states)), min(len(final_states), num_answers)
    )

    correct_answers = random.sample(final_states, num_correct_answers)

    accept_states_answers = [
        {"description": f"$({str(state1)}, {str(state2)})$", "correct": "true"}
        for state1, state2 in correct_answers[:num_correct_answers]
    ]

    accept_states_answers.extend(
        {"description": f"$({str(state1)}, {str(state2)})$", "correct": "false"}
        for state1, state2 in rejecting_states[: num_answers - num_correct_answers]
    )

    data["params"]["first_dfa"] = dfa1.show_diagram().string()
    data["params"]["first_dfa"] = dfa1.show_diagram().string()
    data["params"]["second_dfa"] = generate_dfa_html_description(dfa2)
    data["params"]["transition_start_state_2"] = transition_start_2
    data["params"]["transition_start_state_1"] = transition_start_1
    data["params"]["transition_symbol"] = transition_symbol
    data["params"]["select_dfa_type_answers"] = desc_list
    data["params"]["set_description"] = SET_DESCRIPTIONS[question_type]
    data["params"]["accept_states_answers"] = accept_states_answers

    data["correct_answers"]["end_state_1"] = dfa1.transitions[transition_start_1][ #type: ignore
        transition_symbol
    ]
    data["correct_answers"]["end_state_2"] = dfa2.transitions[transition_start_2][ #type: ignore
        transition_symbol
    ]
    data["correct_answers"]["initial_state_1"] = dfa1.initial_state
    data["correct_answers"]["initial_state_2"] = dfa2.initial_state
