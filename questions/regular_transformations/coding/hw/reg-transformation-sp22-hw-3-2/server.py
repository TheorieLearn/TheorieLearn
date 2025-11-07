import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["commentary"] = (
        r"For example, if $0100101001\textbf{1}0011 \in L$, then $01\textbf{1}001010010011 \in L'$."
    )

    data["params"]["language_description"] = (
        r"$L' = \text{MoveBack}_8(L) = \{xayz : xyaz \in L ~\text{for some}~ x, y, z \in \{0, 1\}^{*} ~\text{and}~ a \in \{0, 1\} ~\text{such that}~ |{y}| \leq 8\}$"
    )

    server_base.generate(data)
