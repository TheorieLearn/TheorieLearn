import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"$$L = \{ 0^i 0^j \mid i, j \in \mathbb{N}, j = \sqrt{i} \}$$"
    )

    server_base.generate(data)
