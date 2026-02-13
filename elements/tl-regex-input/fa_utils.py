# pyright: reportCallIssue=false
from itertools import chain, product
from typing import AbstractSet, Generator, List, Optional, Tuple, Union

from automata.fa.dfa import DFA
from automata.fa.fa import FA
from automata.fa.nfa import NFA
from typing_extensions import assert_never

## DFA/NFA Utilities
LATEX_EPSILON = r"\varepsilon"


def elem_to_latex(elem: str) -> str:
    return elem if elem else LATEX_EPSILON


def strings_of_length_at_most_n(
    lower_bound: int, n: int, *, alphabet: AbstractSet[str] = {"0", "1"}
) -> Generator[str, None, None]:
    return (
        "".join(char_list)
        for char_list in chain.from_iterable(
            product(alphabet, repeat=k) for k in range(lower_bound, n + 1)
        )
    )


def get_equiv_dfa(fsm: Union[DFA, NFA]) -> DFA:
    if isinstance(fsm, NFA):
        return DFA.from_nfa(fsm).to_complete()
    elif isinstance(fsm, DFA):
        return fsm

    assert_never(fsm)


def get_minimum_counterexample(
    input_fa: DFA | NFA, reference_fa: DFA | NFA
) -> Tuple[Optional[str], bool]:
    """
    Takes in two FA, converts them to DFAs (always), and returns a tuple with the counterexample.
    The second element in the tuple is a boolean that is true if the input_fa accepts the counterexample, false otherwise.
    This function returns None for the string if they are equivalent.
    """
    input_dfa = get_equiv_dfa(input_fa)
    reference_dfa = get_equiv_dfa(reference_fa)

    if input_dfa == reference_dfa:
        return (None, False)
    elif input_dfa < reference_dfa:
        diff_dfa = reference_dfa - input_dfa
        return (diff_dfa.random_word(diff_dfa.minimum_word_length()), False)
    else:
        diff_dfa = input_dfa - reference_dfa
        return (diff_dfa.random_word(diff_dfa.minimum_word_length()), True)


def check_dfa(
    submitted_dfa: DFA, reference_dfa: DFA, max_length_to_check: int
) -> Tuple[List[str], List[str]]:
    """
    Parameters
      - submitted_dfa: DFA submitted by the student
      - reference_dfa: Reference DFA for this problem
      - max_length_to_check: Maximum length to check regex string for feedback
    Return value
      - Return a pair of lists of strings: false_positives, false_negatives
    Exceptions
      - Throw ValueError if input symbols don't match or if DFAs are equivalent
    """

    if submitted_dfa.input_symbols != reference_dfa.input_symbols:
        raise ValueError("Input symbols for submitted DFA don't match reference")

    # Brute Force Check
    false_positives: List[str] = []
    false_negatives: List[str] = []

    for bitstring in strings_of_length_at_most_n(
        0, max_length_to_check, alphabet=submitted_dfa.input_symbols
    ):
        accepted_by_reference_DFA = reference_dfa.accepts_input(bitstring)
        accepted_by_submitted_DFA = submitted_dfa.accepts_input(bitstring)

        if not accepted_by_reference_DFA and accepted_by_submitted_DFA:
            false_positives.append(bitstring)
        elif accepted_by_reference_DFA and not accepted_by_submitted_DFA:
            false_negatives.append(bitstring)

    if false_positives or false_negatives:
        return false_positives, false_negatives

    # Graph Based Check
    counterexample, ce_false_positive = get_minimum_counterexample(
        submitted_dfa, reference_dfa
    )

    if counterexample is None:
        raise ValueError("DFAs are equivalent")
    elif ce_false_positive:
        false_positives.append(counterexample)
    else:
        false_negatives.append(counterexample)

    return false_positives, false_negatives


def generate_dfa_feedback_html(
    student_equiv_dfa: DFA,
    reference_equiv_dfa: DFA,
    max_length_to_check: int,
    student_input_name: str,
    *,
    original_student_fa: Optional[FA] = None,
) -> str:
    """
    Generate feedback html for elements. The 'language' here is defined by
    reference_equiv_dfa.
    """

    def latex_prepare_first_n_list(elements: List[str], n: int) -> List[str]:
        "Format a list of strings for display as HTML"

        string_list = ["<ul>\n"]
        string_list.extend(
            f"<li>${elem_to_latex(elem)}$</li>\n" for elem in elements[:n]
        )
        string_list.append("</ul>")
        return string_list

    false_positives, false_negatives = check_dfa(
        student_equiv_dfa, reference_equiv_dfa, max_length_to_check
    )

    assert false_positives or false_negatives
    feedback_string_list = []

    if false_positives:
        feedback_string_list.append(
            f"<p>Here are some strings matched by your {student_input_name} which are not in the language:</p>"
        )
        feedback_string_list.extend(
            latex_prepare_first_n_list(false_positives, max_length_to_check)
        )

        if original_student_fa is not None:
            target_str = false_positives[0]

            input_path, was_acepted = original_student_fa._get_input_path(target_str)

            # Assertion here to make sure this works as expected. TODO remove later.
            assert was_acepted

            # Case where we accept immeditely
            if not input_path:
                assert target_str == ""

                feedback_string_list.append(
                    f"<p>For instance, the string ${elem_to_latex(target_str)}$ was accepted without taking any transitions.</p>"
                )
            else:
                feedback_string_list.append(
                    f"<p>For instance, here's the sequence of states taken to accept the input ${elem_to_latex(target_str)}$:</p>"
                )

                state_sequence_list = ["$$", input_path[0][0]]

                for _, to_state, symbol in input_path:
                    state_sequence_list.append(
                        rf" \xrightarrow{{{elem_to_latex(symbol)}}} "
                    )
                    state_sequence_list.append(str(to_state))

                state_sequence_list.append("$$")

                feedback_string_list.append("".join(state_sequence_list))

    if false_negatives:
        feedback_string_list.append(
            f"<p>Here are some strings in the language which aren't matched by your {student_input_name}:</p>"
        )
        feedback_string_list.extend(
            latex_prepare_first_n_list(false_negatives, max_length_to_check)
        )

    return "".join(feedback_string_list)
