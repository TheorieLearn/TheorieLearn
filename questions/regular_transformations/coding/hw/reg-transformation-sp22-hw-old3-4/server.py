import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["commentary"] = (
        r"Note: For a string $x \in \{0, 1\}^{*}$, "
        + "let $x^F$ denote the string obtained by changing "
        + "all 0's to 1's and all 1's to 0's in $x$."
    )

    data["params"]["language_description"] = (
        r"$L' = \{uv^{F}w : uvw \in L ~\text{for some}~ u, v, w \in \{0, 1\}^{*}\}$"
    )

    server_base.generate(data)
