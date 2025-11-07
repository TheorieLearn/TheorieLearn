# pyright: reportCallIssue=false

from random import randint

import prairielearn as pl
from theorielearn.automata_utils.fa_utils import generate_random_dfa

MAX_RETRIES = 20
MAX_INPUT_STRING_LEN = 6
NUM_RAND_CHOICES = 6


def generate(data: pl.QuestionData) -> None:
    dfa_gen_attempts = 0
    while dfa_gen_attempts < MAX_RETRIES:
        dfa = generate_random_dfa(3, 5)
        dfa_min = dfa.minimum_word_length()
        complement_dfa = dfa.complement()
        cdfa_min = dfa.minimum_word_length()

        if (
            (dfa_min > NUM_RAND_CHOICES or cdfa_min > NUM_RAND_CHOICES)
            or (
                dfa.maximum_word_length() is not None
                and dfa.cardinality() < NUM_RAND_CHOICES
            )
            or (
                complement_dfa.maximum_word_length() is not None
                and complement_dfa.cardinality() < NUM_RAND_CHOICES
            )
        ):
            dfa_gen_attempts += 1
            continue
        break

    data["params"]["dfa"] = str(dfa.show_diagram())

    sampled_accepted: list[str] = []
    sampled_not_accepted: list[str] = []

    attempts = 0

    while len(sampled_accepted) < NUM_RAND_CHOICES:
        try:
            word = dfa.random_word(randint(dfa_min, MAX_INPUT_STRING_LEN))
            if word not in sampled_accepted:
                sampled_accepted.append(word)
        except ValueError:  # noqa: PERF203
            attempts += 1
            if attempts >= MAX_RETRIES:
                break

    while len(sampled_not_accepted) < NUM_RAND_CHOICES:
        try:
            word = complement_dfa.random_word(randint(cdfa_min, MAX_INPUT_STRING_LEN))
            if word not in sampled_not_accepted:
                sampled_not_accepted.append(word)
        except ValueError:  # noqa: PERF203
            attempts += 1
            if attempts >= MAX_RETRIES:
                break

    if "" in sampled_accepted:
        idx = sampled_accepted.index("")
        sampled_accepted[idx] = r"\varepsilon"
    if "" in sampled_not_accepted:
        idx = sampled_not_accepted.index("")
        sampled_not_accepted[idx] = r"\varepsilon"

    data["params"]["strings_in_dfa"] = sampled_accepted
    data["params"]["strings_not_in_dfa"] = sampled_not_accepted
