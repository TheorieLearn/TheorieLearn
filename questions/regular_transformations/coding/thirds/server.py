import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"$L' = \{\mathit{thirds}(w) \mid w \in L\}$"
    )

    data["params"]["commentary"] = (
        r"$\mathit{thirds}(w)$ returns the subsequence of $w$ containing every third symbol. For example, $\mathit{thirds}(011000110) = 100$."
    )

    server_base.generate(data)
