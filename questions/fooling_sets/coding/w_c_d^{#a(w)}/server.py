import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"$$L = \{ wcd^{\text{#}_a(w)} \mid w \in \{a, b\}^{\ast} \}$$"
    )

    server_base.generate(data)
