import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"The set of all palindromes in $(0 + 1)^{\ast}$ whose length is divisible by 3."
    )
    server_base.generate(data)
