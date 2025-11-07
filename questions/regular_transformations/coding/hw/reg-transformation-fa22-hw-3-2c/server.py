import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["commentary"] = (
        r"(i.e. moving an existing 1 forward in the language preserves its regularity)"
    )

    data["params"]["language_description"] = r"$L' = \{x1yz \mid xy1z \in L}$"

    server_base.generate(data)
