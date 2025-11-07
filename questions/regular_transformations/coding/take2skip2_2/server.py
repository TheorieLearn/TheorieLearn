import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"$L' = \{\mathit{take2skip2}(w) \mid w \in L\}$"
    )

    data["params"]["commentary"] = (
        r"$\mathit{take2skip2}(w)$ takes the first two symbols of $w$, skip the next two, takes the next two, skips the next two, and so on. For example, $\mathit{take2skip2}(010)$ = 01."
    )

    server_base.generate(data)
