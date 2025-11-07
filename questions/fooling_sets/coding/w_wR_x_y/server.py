import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"L = $\{ ww^Rxy \mid w,x,y \in \Sigma^+\}$, $\Sigma = \{0, 1\}$"
    )

    server_base.generate(data)
