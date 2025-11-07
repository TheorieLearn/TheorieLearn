import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"$\{ x  \in \{0, 1\}^{\ast} \mid \text{x has odd length at least 3, }$ "
        r"$\text{and the first symbol, the middle symbol, and the last symbol are the same} \}$"
    )

    server_base.generate(data)
