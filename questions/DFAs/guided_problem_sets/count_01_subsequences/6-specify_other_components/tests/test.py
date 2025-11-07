from code_feedback import Feedback
from pl_helpers import name, points
from pl_unit_test import PLTestCase


class Test(PLTestCase):
    @points(1)
    @name("Start state")
    def test_0(self) -> None:
        if type(self.st.start_state) is not tuple or len(self.st.start_state) != 2:
            Feedback.add_feedback("Your start state should be a 2-tuple.")
        elif self.st.start_state != (0, 0):
            Feedback.add_feedback(
                "What values were num0s and num01s initialized to in the pseudocode?"
            )
        else:
            Feedback.set_score(1)

    @points(1)
    @name("0-transitions")
    def test_1(self) -> None:
        for num0s in range(7):
            for num01s in range(7):
                actual = Feedback.call_user(self.st.transition0, num0s, num01s)
                expected = ((num0s + 1) % 7, num01s)

                if actual != expected:
                    Feedback.add_feedback(
                        f"Your answer says that δ(({num0s}, {num01s}), 0) = {actual}, "
                        f"but it should actually be {expected}."
                    )
                    return
        Feedback.set_score(1)

    @points(1)
    @name("1-transitions")
    def test_2(self) -> None:
        for num0s in range(7):
            for num01s in range(7):
                actual = Feedback.call_user(self.st.transition1, num0s, num01s)
                expected = (num0s, (num01s + num0s) % 7)

                if actual != expected:
                    Feedback.add_feedback(
                        f"Your answer says that δ(({num0s}, {num01s}), 1) = {actual}, "
                        f"but it should actually be {expected}."
                    )
                    return
        Feedback.set_score(1)

    @points(1)
    @name("Accept states")
    def test_3(self) -> None:
        for num0s in range(7):
            for num01s in range(7):
                actual = Feedback.call_user(self.st.accept_condition, num0s, num01s)

                if type(actual) is not bool:
                    Feedback.add_feedback(
                        "Your set membership condition is not a boolean."
                    )
                    return

                if num01s == 4 and actual == False:
                    Feedback.add_feedback(
                        f"Your answer says that ({num0s}, {num01s}) is not an accepting state, "
                        f"but it should be an accepting state."
                    )
                    return

                if num01s != 4 and actual == True:
                    Feedback.add_feedback(
                        f"Your answer says that ({num0s}, {num01s}) is an accepting state, "
                        f"but it should not be an accepting state."
                    )
                    return

        Feedback.set_score(1)
