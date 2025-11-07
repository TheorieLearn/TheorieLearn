import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"$$L = \{ ww^Rw \mid w \in \{0, 1\}^{\ast} \}$$"
    )

    server_base.generate(data)
