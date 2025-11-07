# pyright: reportCallIssue=false

import random

import prairielearn as pl
from theorielearn.automata_utils.fa_utils import generate_random_nfa
from theorielearn.shared_utils import (
    grade_question_tokenized,
)


def generate(data: pl.QuestionData) -> None:
    # Generates a random NFA.
    nfa = generate_random_nfa(
        states=6,
        alphabet="01",
        edge_density=0.2,
        epsilon_density=0.4,
        accepting=2,
    )

    # Picks a random state of interest

    state = random.choice(list(nfa.states))

    # Set parameters
    data["params"]["nfa"] = str(nfa.show_diagram())
    data["params"]["state"] = state

    # Generates a string containing the ereach
    data["correct_answers"]["ereach"] = (
        f"{{{','.join(nfa._get_lambda_closures()[state])}}}"
    )


def grade(data: pl.QuestionData) -> None:
    grade_question_tokenized(data, "ereach")
    pl.set_weighted_score_data(data)
