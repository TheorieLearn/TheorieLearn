from itertools import islice

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from typing_extensions import assert_never

LATEX_EPSILON = r"\varepsilon"


def check_dfa(
    submitted_dfa: DFA,
    reference_dfa: DFA,
    max_length_to_check: int,
    max_num_to_check: int,
) -> tuple[list[str], list[str]]:
    """
    Parameters
    ----------
      - submitted_dfa: DFA submitted by the student
      - reference_dfa: Reference DFA for this problem
      - max_length_to_check: Maximum length to check regex string for feedback
      - max_num_to_check: Maximum number of examples of each type to return
    Return value
      - Return a pair of lists of strings: false_positives, false_negatives
    Exceptions
      - Throw ValueError if input symbols don't match or if DFAs are equivalent

    """
    if submitted_dfa.input_symbols != reference_dfa.input_symbols:
        raise ValueError("Input symbols for submitted DFA don't match reference")

    submitted_dfa = submitted_dfa.to_complete()
    reference_dfa = reference_dfa.to_complete()

    false_positive_dfa = submitted_dfa - reference_dfa
    false_negative_dfa = reference_dfa - submitted_dfa

    false_positives = list(
        islice(
            false_positive_dfa.successors(None, max_length=max_length_to_check),
            max_num_to_check,
        )
    )

    false_negatives = list(
        islice(
            false_negative_dfa.successors(None, max_length=max_length_to_check),
            max_num_to_check,
        )
    )

    return false_positives, false_negatives


def get_equiv_dfa(fsm: DFA | NFA) -> DFA:
    if isinstance(fsm, NFA):
        return DFA.from_nfa(fsm)
    elif isinstance(fsm, DFA):
        return fsm

    assert_never(fsm)


def latex_prepare_list(elements: list[str]) -> str:
    """Format a list of strings for display as HTML"""

    def elem_to_latex(elem: str) -> str:
        # Dictionary to translate strings to LaTeX
        translation_dict = {
            "#": r"\#",
            "$": r"\$",
            "%": r"\%",
        }

        if not elem:
            return LATEX_EPSILON

        return "".join(translation_dict.get(char, char) for char in elem)

    string_list = ["<ul>\n"]
    string_list.extend(f"<li>${elem_to_latex(elem)}$</li>\n" for elem in elements)
    string_list.append("</ul>")
    return "".join(string_list)


def generate_dfa_feedback_html(
    student_equiv_dfa: DFA,
    reference_equiv_dfa: DFA,
    max_length_to_check: int,
    max_num_to_check: int,
    student_input_name: str,
) -> str:
    """
    Generate feedback html for elements. The "language" here is defined by
    reference_equiv_dfa.
    """

    assert student_equiv_dfa != reference_equiv_dfa, "DFAs are equivalent"

    false_positives, false_negatives = check_dfa(
        student_equiv_dfa, reference_equiv_dfa, max_length_to_check, max_num_to_check
    )

    feedback_string_list = []

    if false_positives:
        feedback_string_list.extend([
            f"Here are some strings matched by your {student_input_name} which are not in the language:",
            latex_prepare_list(false_positives),
        ])
    if false_negatives:
        feedback_string_list.extend([
            f"Here are some strings in the language which aren't matched by your {student_input_name}:",
            latex_prepare_list(false_negatives),
        ])
    if not false_positives and not false_negatives:
        feedback_string_list.append(
            f"There are no counterexamples of length at most {max_length_to_check}."
        )

    assert feedback_string_list, "Feedback string list is empty"

    return "".join(feedback_string_list)


def compute_partial_credit(
    student_equiv_dfa: DFA,
    reference_equiv_dfa: DFA,
    *,
    word_limit_to_check: int | None = None,
) -> float:
    """
    Compute the approximate density difference between student_equiv_dfa and reference_equiv_dfa.
    Assumes input DFAs are minimal. Used for giving partial credit to students for incorrect answers.
    See section 3.3 for details: https://www.cis.upenn.edu/~alur/Ijcai13.pdf
    """
    if word_limit_to_check is None:
        word_limit_to_check = 2 * len(reference_equiv_dfa.states)

    # Raise exception here to prevent really slow grading / weird freakouts
    if word_limit_to_check > 32:
        raise ValueError(f"Word limit to check {word_limit_to_check} too high.")

    difference_dfa = student_equiv_dfa ^ reference_equiv_dfa

    res = 0.0
    for n in range(word_limit_to_check + 1):
        difference_frac = difference_dfa.count_words_of_length(n) / max(
            reference_equiv_dfa.count_words_of_length(n), 1
        )
        res += difference_frac

    similarity_score = min(1.0, res / (word_limit_to_check + 1))

    return 1.0 - similarity_score
