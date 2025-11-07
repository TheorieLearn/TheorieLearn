import math
from itertools import combinations
from typing import Any

import theorielearn.automata_utils.fa_utils as au
import pytest
from automata.fa.dfa import DFA
from automata.fa.fa import FA
from pytest_lazyfixture import lazy_fixture


@pytest.mark.parametrize(
    "submitted_dfa, reference_dfa",
    combinations(
        lazy_fixture(
            [
                "test_dfa",
                "no_consecutive_11_dfa",
                "zero_or_one_1_dfa",
                "length_at_most_5_dfa",
                "words_ending_in_1_dfa",
            ]
        ),
        2,
    ),
)
@pytest.mark.parametrize("max_length_to_check", [1, 5, 10])
def verify_check_dfa(
    submitted_dfa: DFA, reference_dfa: DFA, max_length_to_check: int
) -> None:
    """Assert that all strings are in the symmetric difference."""
    (false_positives, false_negatives) = au.check_dfa(
        submitted_dfa, reference_dfa, max_length_to_check
    )

    assert len(false_positives + false_negatives) > 0

    false_positive_dfa = submitted_dfa - reference_dfa
    false_negative_dfa = reference_dfa - submitted_dfa

    for x in false_positives:
        assert false_positive_dfa.accepts_input(x)
        assert not false_negative_dfa.accepts_input(x)

    for x in false_negatives:
        assert not false_positive_dfa.accepts_input(x)
        assert false_negative_dfa.accepts_input(x)

    partial_credit = au.compute_partial_credit(submitted_dfa, reference_dfa)

    assert 0.0 <= partial_credit < 1.0


@pytest.mark.parametrize(
    "states, target_string",
    [
        ({"b", "a", "c", 1, 2}, "{1, 2, a, b, c}"),
        (("b", 1, 2, "a"), "(b, 1, 2, a)"),
        ({"a", (1, "b"), ("c", 2), 3}, "{(c, 2), (1, b), 3, a}"),
        (("a", ("c", "b")), "(a, (c, b))"),
        (set(), "∅"),
    ],
)
def verify_states_to_string(states: Any, target_string: str) -> None:
    """Check that states get converted into desired string."""
    assert au.states_to_string(states) == target_string


@pytest.mark.parametrize(
    "fa",
    lazy_fixture(
        [
            "test_dfa",
            "no_consecutive_11_dfa",
            "no_consecutive_11_extra_states_other_dfa",
            "zero_or_one_1_dfa",
            "at_least_three_1_dfa",
            "at_least_four_1_dfa",
            "length_at_most_5_dfa",
            "words_ending_in_1_dfa",
        ]
    ),
)
def verify_sample_input_strings(fa: FA) -> None:
    """Check that sampled strings behave as expected."""

    max_length_to_check = 10
    num_rand_choices = 13
    (accepted, not_accepted) = au.sample_input_strings(
        max_length_to_check, num_rand_choices, fa
    )

    eps = r"\varepsilon"

    # Check invariants for sampled inputs
    assert eps in (accepted + not_accepted)
    assert abs(len(accepted) - len(not_accepted)) <= 2

    # Check accepted and rejected strings
    for x in accepted:
        if x == eps:
            assert fa.accepts_input("")
        else:
            assert fa.accepts_input(x)

        assert len(x) <= max_length_to_check or x == eps

    for x in not_accepted:
        if x == eps:
            assert not fa.accepts_input("")
        else:
            assert not fa.accepts_input(x)

        assert len(x) <= max_length_to_check or x == eps


def verify_compute_partial_credit() -> None:
    dfa1 = DFA(
        states={0, 1, 2, 3, 4, 5, 6},
        input_symbols={"a", "b"},
        transitions={
            0: {"a": 1, "b": 0},
            1: {"a": 1, "b": 2},
            2: {"a": 3, "b": 2},
            3: {"a": 3, "b": 4},
            4: {"a": 5, "b": 4},
            5: {"a": 5, "b": 6},
            6: {"a": 6, "b": 6},
        },
        initial_state=0,
        final_states={4, 5},
    )

    # Weird variable name, comes from original paper
    dfa4 = DFA(
        states={0, 1, 2, 3, 4, 5},
        input_symbols={"a", "b"},
        transitions={
            0: {"a": 1, "b": 0},
            1: {"a": 1, "b": 2},
            2: {"a": 3, "b": 2},
            3: {"a": 3, "b": 4},
            4: {"a": 4, "b": 5},
            5: {"a": 5, "b": 5},
        },
        initial_state=0,
        final_states={4},
    )

    partial_credit = au.compute_partial_credit(dfa4, dfa1)
    assert math.isclose(partial_credit, 0.6782, abs_tol=0.001)
