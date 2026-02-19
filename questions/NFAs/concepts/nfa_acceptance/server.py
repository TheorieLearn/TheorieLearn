# pyright: reportCallIssue=false
import random

import prairielearn as pl
from automata.fa.dfa import DFA
from theorielearn.automata_utils.fa_utils import NFA, generate_random_nfa

MAX_RETRIES = 5
MAX_INPUT_STRING_LEN = 6
NUM_RAND_CHOICES = 6


def load_fallback_nfa():
    """
    Fallback NFA 
    """
    nfa = NFA(
        states={"a", "b", "c", "d", "e", "f"},
        input_symbols={"0", "1"},
        transitions={
            "a": {"0": {"d"}},
            "b": {"0": {"e"}},
            "c": {"1": {"d"}, "": {"f"}},
            "d": {},
            "e": {"0": {"d"}, "1": {"c"}},
            "f": {"1": {"a"}, "0": {"c"}},
        },
        initial_state="b",
        final_states={"e", "f"},
    )

    strings_in_nfa = ["010", "01000", "0100", "0", "01", "010000"]

    strings_not_in_nfa = ["10101", "1", "01110", "000", "101", "11"]

    return nfa, strings_in_nfa, strings_not_in_nfa



def generate(data: pl.QuestionData) -> None:
    nfa_gen_attempts = 0
    while nfa_gen_attempts < MAX_RETRIES:
        nfa = generate_random_nfa(
            states=6, alphabet="01", edge_density=0.2, epsilon_density=0.2, accepting=2
        )
        dfa = DFA.from_nfa(nfa)
        complement_dfa = dfa.complement()
        dfa_min = dfa.minimum_word_length()
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
            nfa_gen_attempts += 1
            continue
        break

    sampled_accepted: list[str] = []
    sampled_not_accepted: list[str] = []

    attempts = 0

    while len(sampled_accepted) < NUM_RAND_CHOICES:
        try:
            word = dfa.random_word(random.randint(dfa_min, MAX_INPUT_STRING_LEN))
            if word not in sampled_accepted:
                sampled_accepted.append(word)
        except ValueError:  # noqa: PERF203
            attempts += 1
            if attempts >= MAX_RETRIES:
                break

    while len(sampled_not_accepted) < NUM_RAND_CHOICES:
        try:
            word = complement_dfa.random_word(
                random.randint(cdfa_min, MAX_INPUT_STRING_LEN)
            )
            if word not in sampled_not_accepted:
                sampled_not_accepted.append(word)
        except ValueError:  # noqa: PERF203
            attempts += 1
            if attempts >= MAX_RETRIES:
                break

    
    # Loading Fallback NFA if random generation fails 

    if len(sampled_accepted) < NUM_RAND_CHOICES or len(sampled_not_accepted) < NUM_RAND_CHOICES:
        nfa, sampled_accepted, sampled_not_accepted = load_fallback_nfa()


    if "" in sampled_accepted:
        idx = sampled_accepted.index("")
        sampled_accepted[idx] = r"\varepsilon"
    if "" in sampled_not_accepted:
        idx = sampled_not_accepted.index("")
        sampled_not_accepted[idx] = r"\varepsilon"


    data["params"]["nfa"] = str(nfa.show_diagram())
    data["params"]["strings_in_nfa"] = sampled_accepted
    data["params"]["strings_not_in_nfa"] = sampled_not_accepted
