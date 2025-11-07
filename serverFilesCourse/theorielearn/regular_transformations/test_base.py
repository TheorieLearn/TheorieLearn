from automata.fa.dfa import DFA, DFATransitionsT
from automata.fa.fa import FA
from theorielearn.automata_utils.fa_utils import (
    generate_dfa_feedback_string,
    get_equiv_dfa,
    states_to_string,
)
from code_feedback import Feedback
from pl_helpers import name, points
from pl_unit_test import PLTestCase
from theorielearn.shared_utils import replace_empty

MAX_LENGTH_TO_CHECK = 10
INPUT_SYMBOLS = {"0", "1"}


def fa_to_string(dfa: FA) -> str:
    res = []

    res.append("States:")
    res.append(f"\tQ = {states_to_string(dfa.states)}")
    res.append("Initial State:")
    res.append(f"\ts = {states_to_string(dfa.initial_state)}")
    res.append("Transitions:")

    for state, transition in dfa.transitions.items():
        for char, destination in transition.items():
            res.append(
                f"\tδ({states_to_string(state)}, {replace_empty(char)}) = {states_to_string(destination)}"
            )
        res.append("")

    res.append("Final States:")
    res.append(f"\t A = {states_to_string(dfa.final_states)}\n")

    return "\n".join(res)


class Test(PLTestCase):
    def check_correctness(self, start_dfa: DFA) -> None:
        reference_equiv_dfa = get_equiv_dfa(self.ref.transform(start_dfa))

        transformed_dfa = Feedback.call_user(self.st.transform, start_dfa)
        student_equiv_dfa = get_equiv_dfa(transformed_dfa)

        if student_equiv_dfa == reference_equiv_dfa:
            Feedback.set_score(1)
            return

        Feedback.add_feedback(
            generate_dfa_feedback_string(
                student_equiv_dfa,
                reference_equiv_dfa,
                MAX_LENGTH_TO_CHECK,
                "transformed FA",
            )
        )

        Feedback.add_feedback(
            "\nHere is the DFA before applying your transform function:"
        )
        Feedback.add_feedback(fa_to_string(start_dfa))
        Feedback.add_feedback("Here is the DFA after applying your transform function:")
        Feedback.add_feedback(fa_to_string(transformed_dfa))

    @points(1)
    @name("L = 0*1*")
    def test_0(self) -> None:
        states = {"notSeen1", "seen1", "fail"}

        transitions: DFATransitionsT = {
            "notSeen1": {"0": "notSeen1", "1": "seen1"},
            "seen1": {"0": "fail", "1": "seen1"},
            "fail": {"0": "fail", "1": "fail"},
        }

        initial_state = "notSeen1"
        final_states = {"notSeen1", "seen1"}

        fa = DFA(
            states=states,
            input_symbols=INPUT_SYMBOLS,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

        self.check_correctness(fa)

    @points(1)
    @name("L = all binary strings where every run of 0s has odd length")
    def test_1(self) -> None:
        states = {"notInRun", "evenRun", "oddRun", "fail"}

        transitions: DFATransitionsT = {
            "notInRun": {"0": "oddRun", "1": "notInRun"},
            "evenRun": {"0": "oddRun", "1": "fail"},
            "oddRun": {"0": "evenRun", "1": "notInRun"},
            "fail": {"0": "fail", "1": "fail"},
        }

        initial_state = "notInRun"
        final_states = {"notInRun", "oddRun"}

        fa = DFA(
            states=states,
            input_symbols=INPUT_SYMBOLS,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

        self.check_correctness(fa)

    @points(1)
    @name("L = all binary strings where every run of 1s has odd length")
    def test_1b(self) -> None:
        states = {"notInRun", "evenRun", "oddRun", "fail"}

        transitions: DFATransitionsT = {
            "notInRun": {"1": "oddRun", "0": "notInRun"},
            "evenRun": {"1": "oddRun", "0": "fail"},
            "oddRun": {"1": "evenRun", "0": "notInRun"},
            "fail": {"1": "fail", "0": "fail"},
        }

        initial_state = "notInRun"
        final_states = {"notInRun", "oddRun"}

        fa = DFA(
            states=states,
            input_symbols=INPUT_SYMBOLS,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

        self.check_correctness(fa)

    @points(1)
    @name(
        "L = all binary strings where every prefix x satisfies |#0(x) - 2*#1(x)| <= 2"
    )
    def test_2(self) -> None:
        states = {-2, -1, 0, 1, 2, "FAIL"}

        transitions: DFATransitionsT = {q: {} for q in states}

        for i in [-2, -1, 0, 1, 2]:
            transitions[i]["0"] = i + 1 if i + 1 <= 2 else "FAIL"
            transitions[i]["1"] = i - 2 if i - 2 >= -2 else "FAIL"

        for a in INPUT_SYMBOLS:
            transitions["FAIL"][a] = "FAIL"

        initial_state = 0
        final_states = states - {"FAIL"}

        fa = DFA(
            states=states,
            input_symbols=INPUT_SYMBOLS,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

        self.check_correctness(fa)

    @points(1)
    @name(
        "L = all binary strings where every prefix x satisfies |#1(x) - 2*#0(x)| <= 2"
    )
    def test_2b(self) -> None:
        states = {-2, -1, 0, 1, 2, "FAIL"}

        transitions: DFATransitionsT = {q: {} for q in states}

        for i in [-2, -1, 0, 1, 2]:
            transitions[i]["1"] = i + 1 if i + 1 <= 2 else "FAIL"
            transitions[i]["0"] = i - 2 if i - 2 >= -2 else "FAIL"

        for a in INPUT_SYMBOLS:
            transitions["FAIL"][a] = "FAIL"

        initial_state = 0
        final_states = states - {"FAIL"}

        fa = DFA(
            states=states,
            input_symbols=INPUT_SYMBOLS,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

        self.check_correctness(fa)

    @points(1)
    @name("L = binary representations of positive integers that are 2 mod 5")
    def test_3(self) -> None:
        states = {i for i in range(5)}

        transitions: DFATransitionsT = {q: {} for q in states}
        for q in states:
            transitions[q]["0"] = (2 * q) % 5
            transitions[q]["1"] = (2 * q + 1) % 5

        initial_state = 0
        final_states = {2}

        fa = DFA(
            states=states,
            input_symbols=INPUT_SYMBOLS,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

        self.check_correctness(fa)

    @points(1)
    @name("L = all binary strings that end with 010")
    def test_4(self) -> None:
        states = {"e", "0", "01", "010"}

        transitions: DFATransitionsT = {
            "e": {"0": "0", "1": "e"},
            "0": {"0": "0", "1": "01"},
            "01": {"0": "010", "1": "e"},
            "010": {"0": "0", "1": "01"},
        }

        initial_state = "e"
        final_states = {"010"}

        fa = DFA(
            states=states,
            input_symbols=INPUT_SYMBOLS,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

        self.check_correctness(fa)
