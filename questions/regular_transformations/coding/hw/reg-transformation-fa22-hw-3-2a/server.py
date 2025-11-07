import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["commentary"] = (
        r"where double(x) denotes the doubling function, which performs a left-shift operation on its input, i.e. double(110100) = 101000."
    )

    data["params"]["language_description"] = r"$L' = \{double(x) \mid x \in L\}$"

    server_base.generate(data)
