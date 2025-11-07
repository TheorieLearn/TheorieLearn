import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"Strings in $(0 + 1 + 2)^{\ast}$ in which no prefex of length 2 or more is a palindrome"
    )
    server_base.generate(data)
