import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"$L' = \{w \in \Sigma^* \mid \mathit{compress}(w) \in L\}$"
    )

    data["params"]["commentary"] = (
        r"$\mathit{compress}(w)$ it takes a string $w$ as input, and returns the string formed by compressing every run of $0$s in $w$ by half."
        + r" Specifically, every run of $2n$ $0$s is compressed to length $n$, and every run of $2n + 1$ $0$s is compressed to length $n + 1$. For example, $\mathit{compress}(11000010) = 110010$."
    )

    server_base.generate(data)
