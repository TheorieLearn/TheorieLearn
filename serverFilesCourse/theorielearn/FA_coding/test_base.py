from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from theorielearn.automata_utils.fa_utils import generate_dfa_feedback_string, get_equiv_dfa
from code_feedback import Feedback
from pl_helpers import name, points
from pl_unit_test import PLTestCase

MAX_LENGTH_TO_CHECK = 10

# Not allowed to switch between NFA and DFA with builtin algorithms
DFA.from_nfa = Feedback.not_allowed  # type: ignore
NFA.from_dfa = Feedback.not_allowed  # type: ignore


class Test(PLTestCase):
    @points(1)
    @name("Check that DFA/NFA is correct")
    def test_0(self) -> None:
        # Check that the type of self.st.fa matches what was requested by the problem
        is_nfa = self.data["params"].get("is_nfa")

        if is_nfa and not isinstance(self.st.fa, NFA):
            Feedback.add_feedback("fa is not an NFA as required")
            return

        # In this case, we need to be working with a DFA
        elif not isinstance(self.st.fa, DFA):
            Feedback.add_feedback("fa is not a DFA as required")
            return

        student_equiv_dfa = get_equiv_dfa(self.st.fa)
        reference_equiv_dfa = get_equiv_dfa(self.ref.fa)

        if student_equiv_dfa == reference_equiv_dfa:
            Feedback.set_score(1)
            return

        student_input_name = "NFA" if is_nfa else "DFA"

        Feedback.add_feedback(
            generate_dfa_feedback_string(
                student_equiv_dfa,
                reference_equiv_dfa,
                MAX_LENGTH_TO_CHECK,
                student_input_name,
            )
        )
