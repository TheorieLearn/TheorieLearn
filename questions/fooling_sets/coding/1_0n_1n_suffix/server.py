import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"L = $\{w$ $\in (0+1)^{\ast} \mid 10^n1^n$ for $n>0$ is a suffix of $w\}$"
    )
    server_base.generate(data)
