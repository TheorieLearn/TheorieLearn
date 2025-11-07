import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = r"$L' = \{\mathit{skip}(w) \mid w \in L\}$"

    data["params"]["commentary"] = (
        r"$\mathit{skip}(w)$ returns the subsequence of $w$ containing only the odd symbols of $w$. For example, $\mathit{skip}(010101) = 000$."
    )

    server_base.generate(data)
