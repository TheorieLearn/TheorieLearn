import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["commentary"] = r"i.e., removes all 1s from the strings of $L$."

    data["params"]["language_description"] = (
        r"$L' = \{0 ^ {\text{#}_0(w)} \mid w \in L\}$"
    )

    server_base.generate(data)
