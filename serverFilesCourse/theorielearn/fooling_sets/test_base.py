from itertools import product

from code_feedback import Feedback
from language_definition import NUM_ELEMENTS_TO_CHECK, isInLanguage
from pl_helpers import name, points
from pl_unit_test import PLTestCase


class Test(PLTestCase):
    @points(1)
    @name("All pairs of distinct elements can be distinguished")
    def test_1(self) -> None:
        # Use a dict to cut down on number of function calls
        student_elem_dict = {
            n: Feedback.call_user(self.st.getFoolingSetElement, n)
            for n in range(1, NUM_ELEMENTS_TO_CHECK + 1)
        }

        # Get a distinguishing suffix for every i and j
        for (i, x), (j, y) in product(
            student_elem_dict.items(), student_elem_dict.items()
        ):
            # Skip if elements are equal
            if i == j:
                continue

            z = Feedback.call_user(self.st.getDistinguishingSuffix, i, j)

            xz = x + z
            yz = y + z

            first_in_language = isInLanguage(xz)
            second_in_language = isInLanguage(yz)

            if first_in_language == second_in_language:
                Feedback.add_feedback(
                    f"When i = {i} and j = {j}, the suffix\n\n"
                    f"z = '{z}'\n\n"
                    f"fails to distinguish the two fooling set elements\n\n"
                    f"x = '{x}'\n"
                    f"y = '{y}'\n"
                )

                if first_in_language and second_in_language:
                    Feedback.add_feedback(
                        f"Both xz = {xz} and yz = {yz} are in the language."
                    )
                else:  # Must be that first_in_language and second_in_language are both false
                    Feedback.add_feedback(
                        f"Both xz = '{xz}' and yz = '{yz}' are not in the language."
                    )

                Feedback.set_score(0)
                return

        Feedback.set_score(1)
