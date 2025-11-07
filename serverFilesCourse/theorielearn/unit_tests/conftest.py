# Define test fixtures for use across all tests.

import automata.fa.dfa as dfa
import automata.fa.nfa as nfa
import pytest
from theorielearn.shared_utils import QuestionData


@pytest.fixture
def test_dfa() -> dfa.DFA:
    "Returns a DFA which matches all binary strings ending in an odd number of '1's"
    return dfa.DFA(
        states={"q0", "q1", "q2"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q0", "1": "q2"},
            "q2": {"0": "q2", "1": "q1"},
        },
        initial_state="q0",
        final_states={"q1"},
    )


@pytest.fixture
def no_consecutive_11_dfa() -> dfa.DFA:
    """
    This DFA accepts all words which do not contain two consecutive occurrences of 1.
    Is a minimal DFA.
    """
    return dfa.DFA(
        states={"p0", "p1", "p2"},
        input_symbols={"0", "1"},
        transitions={
            "p0": {"0": "p0", "1": "p1"},
            "p1": {"0": "p0", "1": "p2"},
            "p2": {"0": "p2", "1": "p2"},
        },
        initial_state="p0",
        final_states={"p0", "p1"},
    )


@pytest.fixture
def no_consecutive_11_extra_states_dfa() -> dfa.DFA:
    """
    This DFA accepts all words which do not contain two consecutive occurrences of 1
    Contains extra states that can be condensed
    """
    return dfa.DFA(
        states={"q0", "q1", "q2", "q3"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q3", "1": "q1"},
            "q1": {"0": "q0", "1": "q2"},
            "q2": {"0": "q2", "1": "q2"},
            "q3": {"0": "q0", "1": "q1"},
        },
        initial_state="q0",
        final_states={"q0", "q1", "q3"},
    )


@pytest.fixture
def no_consecutive_11_extra_states_other_dfa() -> dfa.DFA:
    """
    This DFA accepts all words which do not contain two consecutive occurrences of 1
    Contains extra states that can be condensed
    """
    return dfa.DFA(
        states={"q0", "q1", "q2", "q3"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q0", "1": "q2"},
            "q2": {"0": "q3", "1": "q2"},
            "q3": {"0": "q3", "1": "q2"},
        },
        initial_state="q0",
        final_states={"q0", "q1"},
    )


@pytest.fixture
def zero_or_one_1_dfa() -> dfa.DFA:
    """
    This DFA accepts all words which contain either zero or one occurrence of 1.
    Is a minimal DFA.
    """
    return dfa.DFA(
        states={"q0", "q1", "q2"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q1", "1": "q2"},
            "q2": {"0": "q2", "1": "q2"},
        },
        initial_state="q0",
        final_states={"q0", "q1"},
    )


@pytest.fixture
def at_least_one_1_dfa() -> dfa.DFA:
    """
    This DFA accepts all words which contain at least one occurrence of 1
    """
    return dfa.DFA(
        states={"q0", "q1"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q1", "1": "q1"},
        },
        initial_state="q0",
        final_states={"q1"},
    )


@pytest.fixture
def at_least_three_1_dfa() -> dfa.DFA:
    """
    This DFA accepts all words which contain at least three occurrences of 1.
    Is a minimal DFA.
    """
    return dfa.DFA(
        states={"q0", "q1", "q2", "q3"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q1", "1": "q2"},
            "q2": {"0": "q2", "1": "q3"},
            "q3": {"0": "q3", "1": "q3"},
        },
        initial_state="q0",
        final_states={"q3"},
    )


@pytest.fixture
def at_least_three_1_unreachable_states_dfa() -> dfa.DFA:
    """
    This DFA accepts all words which contain at least three occurrences of 1.
    Is a minimal DFA. Has some unreachable states.
    """
    return dfa.DFA(
        states={"q0", "q1", "q2", "q3", "q4", "q5"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q1", "1": "q2"},
            "q2": {"0": "q2", "1": "q3"},
            "q3": {"0": "q3", "1": "q3"},
            "q4": {"0": "q5", "1": "q5"},
            "q5": {"0": "q4", "1": "q4"},
        },
        initial_state="q0",
        final_states={"q3"},
    )


@pytest.fixture
def empty_language_dfa() -> dfa.DFA:
    """
    This DFA has no reachable final states and therefore accepts the empty language
    """
    return dfa.DFA(
        states={"q0", "q1", "q2", "q3"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q1", "1": "q2"},
            "q2": {"0": "q0", "1": "q1"},
            "q3": {"0": "q2", "1": "q1"},
        },
        initial_state="q0",
        final_states={"q3"},
    )


@pytest.fixture
def rejects_everything_dfa() -> dfa.DFA:
    """
    This DFA has no final states and therefore accepts the empty language
    """
    return dfa.DFA(
        states={"q0", "q1"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q1", "1": "q1"},
            "q1": {"0": "q0", "1": "q0"},
        },
        initial_state="q0",
        final_states=set(),
    )


@pytest.fixture
def rejects_everything_dfa_minimal() -> dfa.DFA:
    """
    This DFA has no final states and therefore accepts the empty language.
    Is a minimal version of the above DFA.
    """
    return dfa.DFA(
        states={frozenset(("q0", "q1"))},
        input_symbols={"0", "1"},
        transitions={
            frozenset(("q0", "q1")): {
                "0": frozenset(("q0", "q1")),
                "1": frozenset(("q0", "q1")),
            }
        },
        initial_state=frozenset(("q0", "q1")),
        final_states=set(),
    )


@pytest.fixture
def accepts_everything_dfa() -> dfa.DFA:
    """
    This DFA accepts all binary strings
    """
    return dfa.DFA(
        states={"q0"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q0"},
        },
        initial_state="q0",
        final_states={"q0"},
    )


@pytest.fixture
def accepts_everything_extra_states_dfa() -> dfa.DFA:
    """
    This DFA accepts all binary strings. Contains extra states.
    """
    return dfa.DFA(
        states={"q0", "q1", "q2", "q3", "q4", "q5", "q6"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q1", "1": "q1"},
            "q1": {"0": "q2", "1": "q2"},
            "q2": {"0": "q3", "1": "q3"},
            "q3": {"0": "q4", "1": "q4"},
            "q4": {"0": "q5", "1": "q5"},
            "q5": {"0": "q6", "1": "q6"},
            "q6": {"0": "q6", "1": "q6"},
        },
        initial_state="q0",
        final_states={"q0", "q1", "q2", "q3", "q4", "q5", "q6"},
    )


@pytest.fixture
def at_least_four_1_dfa() -> dfa.DFA:
    """
    This DFA accepts all words which contain at least four occurrences of 1
    """
    return dfa.DFA(
        states={"q0", "q1", "q2", "q3", "q4"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q1", "1": "q2"},
            "q2": {"0": "q2", "1": "q3"},
            "q3": {"0": "q3", "1": "q4"},
            "q4": {"0": "q4", "1": "q4"},
        },
        initial_state="q0",
        final_states={"q4"},
    )


@pytest.fixture
def length_at_most_5_dfa() -> dfa.DFA:
    """
    This DFA accepts all binary strings which have length less than or equal to 5
    """
    return dfa.DFA(
        states={"q0", "q1", "q2", "q3", "q4", "q5", "q6"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q1", "1": "q1"},
            "q1": {"0": "q2", "1": "q2"},
            "q2": {"0": "q3", "1": "q3"},
            "q3": {"0": "q4", "1": "q4"},
            "q4": {"0": "q5", "1": "q5"},
            "q5": {"0": "q6", "1": "q6"},
            "q6": {"0": "q6", "1": "q6"},
        },
        initial_state="q0",
        final_states={"q0", "q1", "q2", "q3", "q4", "q5"},
    )


@pytest.fixture
def words_ending_in_1_dfa() -> dfa.DFA:
    """
    This DFA just accepts words ending in 1. Is a minimal DFA.
    """
    return dfa.DFA(
        states={"q0", "q1"},
        input_symbols={"0", "1"},
        transitions={"q0": {"0": "q0", "1": "q1"}, "q1": {"0": "q0", "1": "q1"}},
        initial_state="q0",
        final_states={"q1"},
    )


@pytest.fixture
def length_at_least_2_dfa() -> dfa.DFA:
    """
    This DFA accepts all words which are at least two characters long.
    The states q1/q2 and q3/q4/q5/q6 are redundant.
    The state q7 is not reachable.
    """
    return dfa.DFA(
        states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q1", "1": "q2"},
            "q1": {"0": "q3", "1": "q4"},
            "q2": {"0": "q5", "1": "q6"},
            "q3": {"0": "q3", "1": "q3"},
            "q4": {"0": "q4", "1": "q4"},
            "q5": {"0": "q5", "1": "q5"},
            "q6": {"0": "q6", "1": "q6"},
            "q7": {"0": "q7", "1": "q7"},
        },
        initial_state="q0",
        final_states={"q3", "q4", "q5", "q6"},
    )


@pytest.fixture
def length_at_least_2_dfa_minimal() -> dfa.DFA:
    """
    This DFA accepts all words which are at least two characters long.
    Is a minimal version of the above DFA.
    """
    return dfa.DFA(
        states={
            frozenset(("q0",)),
            frozenset(("q1", "q2")),
            frozenset(("q3", "q4", "q5", "q6")),
        },
        input_symbols={"0", "1"},
        transitions={
            frozenset(("q0",)): {
                "0": frozenset(("q1", "q2")),
                "1": frozenset(("q1", "q2")),
            },
            frozenset(("q1", "q2")): {
                "0": frozenset(("q3", "q4", "q5", "q6")),
                "1": frozenset(("q3", "q4", "q5", "q6")),
            },
            frozenset(("q3", "q4", "q5", "q6")): {
                "0": frozenset(("q3", "q4", "q5", "q6")),
                "1": frozenset(("q3", "q4", "q5", "q6")),
            },
        },
        initial_state=frozenset(("q0",)),
        final_states={frozenset(("q3", "q4", "q5", "q6"))},
    )


@pytest.fixture
def all_words_dfa() -> dfa.DFA:
    """
    This DFA accepts all words with ones and zeroes.
    The two states can be merged into one.
    """
    return dfa.DFA(
        states={"q0", "q1"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q1", "1": "q1"},
            "q1": {"0": "q0", "1": "q0"},
        },
        initial_state="q0",
        final_states={"q0", "q1"},
    )


@pytest.fixture
def all_words_dfa_minimal() -> dfa.DFA:
    """
    This DFA accepts all words with ones and zeroes. Is a minimal DFA.
    """
    return dfa.DFA(
        states={frozenset(("q0", "q1"))},
        input_symbols={"0", "1"},
        transitions={
            frozenset(("q0", "q1")): {
                "0": frozenset(("q0", "q1")),
                "1": frozenset(("q0", "q1")),
            }
        },
        initial_state=frozenset(("q0", "q1")),
        final_states={frozenset(("q0", "q1"))},
    )


@pytest.fixture
def large_dfa() -> dfa.DFA:
    """
    Very large DFA
    """
    return dfa.DFA(
        states={
            "13",
            "56",
            "18",
            "10",
            "15",
            "26",
            "24",
            "54",
            "32",
            "27",
            "5",
            "43",
            "8",
            "3",
            "17",
            "45",
            "57",
            "46",
            "35",
            "9",
            "0",
            "21",
            "39",
            "51",
            "6",
            "55",
            "47",
            "11",
            "20",
            "12",
            "59",
            "38",
            "44",
            "52",
            "16",
            "41",
            "1",
            "4",
            "28",
            "58",
            "48",
            "23",
            "22",
            "2",
            "31",
            "36",
            "34",
            "49",
            "40",
            "7",
            "25",
            "30",
            "53",
            "42",
            "33",
            "19",
            "50",
            "37",
            "14",
            "29",
        },
        input_symbols={"L", "U", "R", "D"},
        transitions={
            "55": {"L": "20", "U": "49", "R": "20", "D": "49"},
            "57": {"L": "5", "U": "6", "R": "1", "D": "46"},
            "35": {"L": "44", "U": "32", "R": "36", "D": "33"},
            "13": {"L": "45", "U": "23", "R": "45", "D": "23"},
            "43": {"L": "44", "U": "32", "R": "44", "D": "33"},
            "9": {"L": "5", "U": "6", "R": "1", "D": "6"},
            "53": {"L": "20", "U": "33", "R": "20", "D": "32"},
            "12": {"L": "40", "U": "23", "R": "25", "D": "11"},
            "42": {"L": "1", "U": "49", "R": "5", "D": "49"},
            "24": {"L": "40", "U": "48", "R": "25", "D": "23"},
            "27": {"L": "5", "U": "46", "R": "1", "D": "6"},
            "22": {"L": "40", "U": "48", "R": "25", "D": "11"},
            "19": {"L": "36", "U": "32", "R": "44", "D": "33"},
            "59": {"L": "40", "U": "48", "R": "45", "D": "11"},
            "39": {"L": "45", "U": "48", "R": "25", "D": "11"},
            "51": {"L": "20", "U": "18", "R": "20", "D": "18"},
            "34": {"L": "5", "U": "4", "R": "1", "D": "31"},
            "33": {"L": "44", "U": "0", "R": "36", "D": "28"},
            "23": {"L": "45", "U": "8", "R": "45", "D": "8"},
            "46": {"L": "44", "U": "0", "R": "44", "D": "28"},
            "58": {"L": "5", "U": "4", "R": "1", "D": "4"},
            "50": {"L": "20", "U": "28", "R": "20", "D": "0"},
            "54": {"L": "40", "U": "8", "R": "25", "D": "41"},
            "49": {"L": "1", "U": "18", "R": "5", "D": "18"},
            "21": {"L": "40", "U": "26", "R": "25", "D": "8"},
            "16": {"L": "5", "U": "31", "R": "1", "D": "4"},
            "6": {"L": "40", "U": "26", "R": "25", "D": "41"},
            "32": {"L": "36", "U": "0", "R": "44", "D": "28"},
            "48": {"L": "40", "U": "26", "R": "45", "D": "41"},
            "11": {"L": "45", "U": "26", "R": "25", "D": "41"},
            "15": {"L": "14", "U": "49", "R": "14", "D": "49"},
            "1": {"L": "56", "U": "6", "R": "37", "D": "46"},
            "3": {"L": "4", "U": "32", "R": "17", "D": "33"},
            "45": {"L": "8", "U": "23", "R": "8", "D": "23"},
            "52": {"L": "4", "U": "32", "R": "4", "D": "33"},
            "36": {"L": "56", "U": "6", "R": "37", "D": "6"},
            "20": {"L": "14", "U": "33", "R": "14", "D": "32"},
            "25": {"L": "47", "U": "23", "R": "10", "D": "11"},
            "29": {"L": "37", "U": "49", "R": "56", "D": "49"},
            "40": {"L": "47", "U": "48", "R": "10", "D": "23"},
            "5": {"L": "56", "U": "46", "R": "37", "D": "6"},
            "44": {"L": "47", "U": "48", "R": "10", "D": "11"},
            "38": {"L": "17", "U": "32", "R": "4", "D": "33"},
            "2": {"L": "47", "U": "48", "R": "8", "D": "11"},
            "30": {"L": "8", "U": "48", "R": "10", "D": "11"},
            "7": {"L": "14", "U": "18", "R": "14", "D": "18"},
            "37": {"L": "56", "U": "4", "R": "37", "D": "31"},
            "28": {"L": "4", "U": "0", "R": "17", "D": "28"},
            "8": {"L": "8", "U": "8", "R": "8", "D": "8"},
            "31": {"L": "4", "U": "0", "R": "4", "D": "28"},
            "17": {"L": "56", "U": "4", "R": "37", "D": "4"},
            "14": {"L": "14", "U": "28", "R": "14", "D": "0"},
            "10": {"L": "47", "U": "8", "R": "10", "D": "41"},
            "18": {"L": "37", "U": "18", "R": "56", "D": "18"},
            "47": {"L": "47", "U": "26", "R": "10", "D": "8"},
            "56": {"L": "56", "U": "31", "R": "37", "D": "4"},
            "4": {"L": "47", "U": "26", "R": "10", "D": "41"},
            "0": {"L": "17", "U": "0", "R": "4", "D": "28"},
            "26": {"L": "47", "U": "26", "R": "8", "D": "41"},
            "41": {"L": "8", "U": "26", "R": "10", "D": "41"},
        },
        initial_state="55",
        final_states={
            "15",
            "24",
            "54",
            "32",
            "27",
            "5",
            "43",
            "57",
            "3",
            "46",
            "35",
            "9",
            "21",
            "39",
            "51",
            "6",
            "55",
            "11",
            "20",
            "12",
            "59",
            "38",
            "44",
            "52",
            "16",
            "1",
            "58",
            "48",
            "22",
            "2",
            "36",
            "34",
            "49",
            "40",
            "25",
            "30",
            "53",
            "42",
            "33",
            "19",
            "50",
            "29",
        },
    )


@pytest.fixture
def large_dfa_minimal() -> dfa.DFA:
    """
    A minimal version of the very large DFA
    """
    return dfa.DFA(
        states={
            frozenset(("5",)),
            frozenset(("36",)),
            frozenset(("1",)),
            frozenset(("49",)),
            frozenset(("40",)),
            frozenset(("25",)),
            frozenset(("46",)),
            frozenset(("6",)),
            frozenset(("55",)),
            frozenset(
                (
                    "0",
                    "10",
                    "14",
                    "17",
                    "18",
                    "23",
                    "26",
                    "28",
                    "31",
                    "37",
                    "4",
                    "41",
                    "45",
                    "47",
                    "56",
                    "8",
                )
            ),
            frozenset(("33",)),
            frozenset(("11",)),
            frozenset(("20",)),
            frozenset(("48",)),
            frozenset(("44",)),
            frozenset(("32",)),
        },
        input_symbols={"L", "U", "R", "D"},
        transitions={
            frozenset(("48",)): {
                "L": frozenset(("40",)),
                "U": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "R": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "D": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
            },
            frozenset(("44",)): {
                "L": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "U": frozenset(("48",)),
                "R": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "D": frozenset(("11",)),
            },
            frozenset(("40",)): {
                "L": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "U": frozenset(("48",)),
                "R": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "D": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
            },
            frozenset(("33",)): {
                "L": frozenset(("44",)),
                "U": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "R": frozenset(("36",)),
                "D": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
            },
            frozenset(("55",)): {
                "L": frozenset(("20",)),
                "U": frozenset(("49",)),
                "R": frozenset(("20",)),
                "D": frozenset(("49",)),
            },
            frozenset(("32",)): {
                "L": frozenset(("36",)),
                "U": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "R": frozenset(("44",)),
                "D": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
            },
            frozenset(("46",)): {
                "L": frozenset(("44",)),
                "U": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "R": frozenset(("44",)),
                "D": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
            },
            frozenset(("25",)): {
                "L": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "U": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "R": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "D": frozenset(("11",)),
            },
            frozenset(("6",)): {
                "L": frozenset(("40",)),
                "U": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "R": frozenset(("25",)),
                "D": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
            },
            frozenset(("11",)): {
                "L": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "U": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "R": frozenset(("25",)),
                "D": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
            },
            frozenset(("5",)): {
                "L": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "U": frozenset(("46",)),
                "R": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "D": frozenset(("6",)),
            },
            frozenset(("49",)): {
                "L": frozenset(("1",)),
                "U": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "R": frozenset(("5",)),
                "D": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
            },
            frozenset(
                (
                    "0",
                    "10",
                    "14",
                    "17",
                    "18",
                    "23",
                    "26",
                    "28",
                    "31",
                    "37",
                    "4",
                    "41",
                    "45",
                    "47",
                    "56",
                    "8",
                )
            ): {
                "L": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "U": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "R": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "D": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
            },
            frozenset(("20",)): {
                "L": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "U": frozenset(("33",)),
                "R": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "D": frozenset(("32",)),
            },
            frozenset(("36",)): {
                "L": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "U": frozenset(("6",)),
                "R": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "D": frozenset(("6",)),
            },
            frozenset(("1",)): {
                "L": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "U": frozenset(("6",)),
                "R": frozenset(
                    (
                        "0",
                        "10",
                        "14",
                        "17",
                        "18",
                        "23",
                        "26",
                        "28",
                        "31",
                        "37",
                        "4",
                        "41",
                        "45",
                        "47",
                        "56",
                        "8",
                    )
                ),
                "D": frozenset(("46",)),
            },
        },
        initial_state=frozenset(("55",)),
        final_states={
            frozenset(("5",)),
            frozenset(("1",)),
            frozenset(("36",)),
            frozenset(("49",)),
            frozenset(("40",)),
            frozenset(("25",)),
            frozenset(("46",)),
            frozenset(("6",)),
            frozenset(("55",)),
            frozenset(("33",)),
            frozenset(("11",)),
            frozenset(("20",)),
            frozenset(("48",)),
            frozenset(("44",)),
            frozenset(("32",)),
        },
    )


@pytest.fixture
def test_nfa() -> nfa.NFA:
    """
    Returns an NFA which matches strings beginning with 'a', ending with 'a', and
    containing no consecutive 'b's
    """
    return nfa.NFA(
        states={"q0", "q1", "q2"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": {"q1"}},
            "q1": {"a": {"q1"}, "": {"q2"}},
            "q2": {"b": {"q0"}},
        },
        initial_state="q0",
        final_states={"q1"},
    )


# ---------------------------- Fixtrues for regex tests ------------------------
@pytest.fixture
def regex_1_nfa() -> nfa.NFA:
    """
    Returns an NFA matching the regex (01 + 1)*(0*1 + 1*0)(10 + 0)*.
    """
    return nfa.NFA(
        states={"s", "a", "b", "c", "d", "e"},
        input_symbols={"0", "1"},
        transitions={
            "s": {"0": {"a"}, "1": {"s"}, "": {"b", "d"}},
            "a": {"1": {"s"}},
            "b": {"0": {"b"}, "1": {"c"}},
            "c": {"0": {"c"}, "1": {"e"}},
            "d": {"0": {"c"}, "1": {"d"}},
            "e": {"0": {"c"}},
        },
        initial_state="s",
        final_states={"c"},
    )


@pytest.fixture
def regex_2_nfa() -> nfa.NFA:
    """
    Returns an NFA matching the regex (1(010)*(11)* + 010)*.
    """
    return nfa.NFA(
        states={"s", "a", "b", "c", "d", "e", "f", "g", "h"},
        input_symbols={"0", "1"},
        transitions={
            "s": {"0": {"g"}, "1": {"a"}},
            "a": {"0": {"b"}, "": {"d"}},
            "b": {"1": {"c"}},
            "c": {"0": {"a"}},
            "d": {"1": {"e"}, "": {"f"}},
            "e": {"1": {"d"}},
            "f": {"": {"s"}},
            "g": {"1": {"h"}},
            "h": {"0": {"f"}},
        },
        initial_state="s",
        final_states={"s"},
    )


@pytest.fixture
def regex_3_dfa() -> dfa.DFA:
    """
    Returns a DFA matching the regex 0(0 + 1)*0 + 1(0 + 1)*1.
    """
    return dfa.DFA(
        states={"s", "0", "1", "00", "01", "10", "11"},
        input_symbols={"0", "1"},
        transitions={
            "s": {"0": "0", "1": "1"},
            "0": {"0": "00", "1": "01"},
            "1": {"0": "10", "1": "11"},
            "00": {"0": "00", "1": "01"},
            "01": {"0": "00", "1": "01"},
            "10": {"0": "10", "1": "11"},
            "11": {"0": "10", "1": "11"},
        },
        initial_state="s",
        final_states={"00", "11"},
    )


@pytest.fixture
def regex_4_dfa() -> dfa.DFA:
    """
    Returns a DFA matching the regex (0 + 1)*00 + (0 + 1)*11.
    """
    return dfa.DFA(
        states={"s", "0", "1", "00", "01", "10", "11"},
        input_symbols={"0", "1"},
        transitions={
            "s": {"0": "0", "1": "1"},
            "0": {"0": "00", "1": "01"},
            "1": {"0": "10", "1": "11"},
            "00": {"0": "00", "1": "01"},
            "01": {"0": "10", "1": "11"},
            "10": {"0": "00", "1": "01"},
            "11": {"0": "10", "1": "11"},
        },
        initial_state="s",
        final_states={"00", "11"},
    )


@pytest.fixture
def regex_5_nfa() -> nfa.NFA:
    """
    Returns a NFA matching the regex (((01)*0+2)(100)*1)*(1*+0*2*).
    """
    return nfa.NFA(
        states={"s", "a", "b", "c", "d", "e", "f", "g", "h"},
        input_symbols={"0", "1", "2"},
        transitions={
            "s": {"": {"a", "f", "g"}, "2": {"c"}},
            "a": {"0": {"b", "c"}},
            "b": {"1": {"a"}},
            "c": {"1": {"s", "d"}},
            "d": {"0": {"e"}},
            "e": {"0": {"c"}},
            "f": {"1": {"f"}},
            "g": {"0": {"g"}, "": {"h"}},
            "h": {"2": {"h"}},
        },
        initial_state="s",
        final_states={"f", "h"},
    )


@pytest.fixture
def question_data() -> QuestionData:
    """
    Prepare data dict
    """
    data: QuestionData = {
        "params": dict(),
        "correct_answers": dict(),
        "submitted_answers": dict(),
        "format_errors": dict(),
        "partial_scores": dict(),
        "score": 0.0,
        "feedback": dict(),
        "variant_seed": 0,
        "options": dict(),
        "raw_submitted_answers": dict(),
        "editable": False,
        "panel": "question",
        "extensions": dict(),
        "ai_grading": False,
        "answers_names": dict(),
        "num_valid_submissions": 0,
        "manual_grading": False
    }

    return data
