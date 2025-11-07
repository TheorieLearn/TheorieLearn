import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = r"$L' = \{w : ww \in L\}$"

    server_base.generate(data)
