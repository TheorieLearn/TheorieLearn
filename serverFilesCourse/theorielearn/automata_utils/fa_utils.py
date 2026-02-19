import math
import string
from itertools import product
from random import choice, randint, random, sample, shuffle
from typing import Any, List, Optional, Set, Tuple, Union

import automata.base.exceptions as exceptions
import networkx as nx
from automata.fa.dfa import DFA, DFAStateT, DFATransitionsT
from automata.fa.fa import FA
from automata.fa.nfa import NFA, NFAStateT
from theorielearn.shared_utils import replace_empty, strings_of_length_at_most_n
from typing_extensions import assert_never

LATEX_EPSILON = r"\varepsilon"


def elem_to_latex(elem: str) -> str:
    return elem if elem else LATEX_EPSILON


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


def states_to_string(obj: Any) -> str:
    if isinstance(obj, frozenset):
        obj = set(obj)

    if isinstance(obj, set):
        if not obj:
            return "∅"

        # Weird highlighting, but code inside braces is indeed run
        return (
            f"{{{', '.join(states_to_string(item) for item in sorted(obj, key=str))}}}"
        )

    elif isinstance(obj, tuple):
        if not obj:
            raise ValueError("Tuple shouldn't be empty")
        return f"({', '.join(states_to_string(item) for item in obj)})"

    return replace_empty(str(obj))


def sample_input_strings(
    max_input_string_len: int, num_rand_choices: int, fa: FA
) -> Tuple[List[str], List[str]]:
    """
    Samples accepted and not accepted input strings for the given fa. Converts
    for display on the frontend.
    """

    # Get all accepted and non-accepted strings of length at most n
    accepted = []
    not_accepted = []

    for x in strings_of_length_at_most_n(
        1, max_input_string_len, alphabet=fa.input_symbols
    ):
        if fa.accepts_input(x):
            accepted.append(x)
        else:
            not_accepted.append(x)

    # Next, do random sampling based on the number of accepted and rejected strings
    sampled_accepted = []
    sampled_not_accepted = []

    if len(accepted) < (num_rand_choices // 2):
        sampled_accepted = accepted
        sampled_not_accepted = sample(not_accepted, num_rand_choices - len(accepted))

    elif len(not_accepted) < (num_rand_choices // 2 + num_rand_choices % 2):
        sampled_accepted = sample(accepted, num_rand_choices - len(not_accepted))
        sampled_not_accepted = not_accepted

    else:
        sampled_accepted = sample(accepted, num_rand_choices // 2)
        sampled_not_accepted = sample(
            not_accepted, num_rand_choices // 2 + num_rand_choices % 2
        )

    # Always include the empty string
    if fa.accepts_input(""):
        sampled_accepted.append(LATEX_EPSILON)
    else:
        sampled_not_accepted.append(LATEX_EPSILON)

    # Return the result
    return sampled_accepted, sampled_not_accepted


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
        return (diff_dfa.random_word(diff_dfa.minimum_word_length()), False)  # type: ignore
    else:
        diff_dfa = input_dfa - reference_dfa
        return (diff_dfa.random_word(diff_dfa.minimum_word_length()), True)  # type: ignore


def generate_dfa_feedback_string(
    student_equiv_dfa: DFA,
    reference_equiv_dfa: DFA,
    max_length_to_check: int,
    student_input_name: str,
) -> str:
    """
    Generate a feedback string for use by externally graded questions. The
    'language' here is defined by reference_equiv_dfa.
    """

    res = []

    false_positives, false_negatives = check_dfa(
        student_equiv_dfa, reference_equiv_dfa, max_length_to_check
    )

    assert false_positives or false_negatives

    if false_positives:
        res.append(
            f"Here are some strings matched by your {student_input_name}"
            " which are not in the language:"
        )

        for x in false_positives[:max_length_to_check]:
            res.append(replace_empty(x))

        # Add blank line between false positives and false negatives, if both exist
        if false_negatives:
            res.append("")

    if false_negatives:
        res.append(
            "Here are some strings in the language which"
            f" aren't matched by your {student_input_name}:"
        )

        for x in false_negatives[:max_length_to_check]:
            res.append(replace_empty(x))

    return "\n".join(res)


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


def compute_partial_credit(
    student_equiv_dfa: DFA,
    reference_equiv_dfa: DFA,
    *,
    word_limit_to_check: Optional[int] = None,
) -> float:
    """
    Computes the approximate density difference between student_equiv_dfa and reference_equiv_dfa.
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


def generate_random_dfa(lower: int, upper: int) -> DFA:
    """
    Generates a random DFA with n states, where lower <= n <= upper, over the alphabet {0, 1}.
    @param lower
        minimum number of states
    @param upper
        maximum number of states
    @return DFA object
        Randomly generated DFA.
    """
    # TODO: Use rejection sampling instead of creating a Hamiltonian path from the start state.

    n = randint(lower, upper)
    input_symbols = {"0", "1"}
    states = set(range(n))
    random_state_ordering = list(states)
    shuffle(random_state_ordering)

    initial_state = random_state_ordering[0]
    transitions: DFATransitionsT = {i: dict() for i in range(n)}

    # Fill in transitions so that start state can reach all other states.
    for i in range(n - 1):
        symbol = str(randint(0, 1))
        origin_state, destination_state = (
            random_state_ordering[i],
            random_state_ordering[i + 1],
        )
        transitions[origin_state][symbol] = destination_state

    # Fill in remaining transitions.
    for transition, symbol in product(transitions.values(), input_symbols):
        if symbol not in transition:
            transition[symbol] = randint(0, n - 1)

    # Generate accepting states.
    final_states = {state for state in states if randint(0, 1)}

    # Enforce at least one accepting state and at least one rejecting state.
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


def generate_random_nfa(
    states: int,
    alphabet: str,
    edge_density: float,
    epsilon_density: float,
    accepting: int,
) -> NFA:
    def int_to_lower(n: int) -> str:
        return chr(n + 97)

    # We shouldn't need random NFAs more than 26 states.
    state_max = 26

    if not (1 <= states < state_max):
        raise ValueError("Cannot request an NFA with more than 26 states")
    elif not (1 <= accepting <= states):
        raise ValueError(
            f"Cannot have {accepting} accept states in an NFA with {states} states"
        )
    elif not (0 <= edge_density <= 1.0):
        raise ValueError(f"Edge density {edge_density} is not in the range [0.0, 1.0]")
    elif not (0 <= epsilon_density <= 1.0):
        raise ValueError(
            f"Edge density {epsilon_density} is not in the range [0.0, 1.0]"
        )

    # Pick a number of edges between states and states*sqrt(states) (avoiding dense graphs)
    edges = int(math.ceil(((states ** (1.5) - states) * edge_density) + states))

    nfa = None
    while nfa is None:
        # Generate random graph until we find one with start state reachable to every other state
        G: Optional[nx.Graph] = None
        start = None
        while start is None:
            G = nx.gnm_random_graph(states, edges, directed=True)
            assert G is not None
            start_candidates = list(range(states))
            shuffle(start_candidates)
            for candidate in start_candidates:
                if len(nx.shortest_path(G, source=candidate)) == states:
                    start = candidate
                    break

        assert G is not None

        # Assign all the nodes a state in the transitions dict.
        transitions = {int_to_lower(v): dict() for v in G.nodes}

        # Assign symbols to all the edges in the graph, choosing epsilons occasionally.
        for u, v in G.edges:
            symbol = "" if random() < epsilon_density else choice(alphabet)
            transitions[int_to_lower(u)].setdefault(symbol, set()).add(int_to_lower(v))

        # Create NFA data structures
        nfa_states = set(string.ascii_lowercase[:states])
        input_symbols = set(alphabet)
        initial_state = int_to_lower(start)
        final_states = set(string.ascii_lowercase[(states - accepting) : states])

        nfa = NFA(
            states=nfa_states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )
        equiv_dfa = DFA.from_nfa(nfa, retain_names=False)
        equiv_dfa_comp = equiv_dfa.complement()

        # Check to see if NFA both accepts and rejects strings, if not start over
        if equiv_dfa_comp.isempty() or equiv_dfa.isempty():  # type: ignore
            nfa = None

    return nfa


def generate_dfa_html_description(dfa: DFA) -> str:
    """
    Generates an HTML-based description of the input DFA. Assumes the alphabet is {'0', '1'}.
    @return string
        Description of the input DFA, including a transition table, its accepting states, and its start state.
    """
    table_header = """
    <table border=\"1px solid black\" style=\"width:30%;text-align:center\">
        <tr>
            <th></th>
            <th>'0'</th>
            <th>'1'</th>
        </tr>
    """
    table_footer = "</table>"

    dfa_description_list = ["The transition table is as follows: ", table_header]
    for state in dfa.states:
        dfa_description_list.append("<tr>")
        for entry in [
            f"State {str(state)}",
            str(dfa.transitions[state]["0"]),
            str(dfa.transitions[state]["1"]),
        ]:
            dfa_description_list.append(f"<td>{entry}</td>")
        dfa_description_list.append("</tr>")
    dfa_description_list.append(table_footer)

    accepting_state_string = ", ".join(str(state) for state in sorted(dfa.final_states))
    dfa_description_list.append(
        f"The set of accepting states is ${{{accepting_state_string}}}$.<br>"
    )
    dfa_description_list.append(f"The start state is state ${str(dfa.initial_state)}$.")
    return "".join(dfa_description_list)


def dfa_read_input_from_state(dfa: DFA, state: DFAStateT, input: str) -> DFAStateT:
    """
    Read in an input from a valid state of the DFA

    Return the resulting state after reading the input.
    """

    new_dfa = DFA(
        states=dfa.states,
        input_symbols=dfa.input_symbols,
        transitions=dfa.transitions,
        initial_state=state,
        final_states=dfa.states,
    )

    return new_dfa.read_input(input)


def nfa_read_input_from_state(nfa: NFA, state: NFAStateT, input: str) -> Set[NFAStateT]:
    """
    Read in an input from a valid state of the NFA

    Return the resulting state after reading the input.
    """

    new_nfa = NFA(
        states=nfa.states,
        input_symbols=nfa.input_symbols,
        transitions=nfa.transitions,
        initial_state=state,
        final_states=nfa.states,
    )

    try:
        return new_nfa.read_input(input)
    except exceptions.RejectionException:
        return set()
