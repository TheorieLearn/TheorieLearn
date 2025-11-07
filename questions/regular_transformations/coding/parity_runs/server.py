import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData

def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"$L' = \{w \in \Sigma^\ast \mid \mathit{parity\_runs}(w) \in L\}$"
    )

    data["params"]["commentary"] = (
        r"$\mathit{parity\_runs}(w)$ returns the string formed by replacing each maximal substring of identical bits in $w$ with $1$ if the length of the substring is odd, and with $0$ if the length is even. "
        + r"For example, $\mathit{parity\_runs}(11000010) = 0011$."
    )

    server_base.generate(data)
