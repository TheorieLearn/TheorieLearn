import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"L = $\{x \in \{0, 1\}^{\ast} \mid \text{min }(\#_0(x), \#_1(x)) \text{ is divisible by } 5\}$"
    )

    server_base.generate(data)
