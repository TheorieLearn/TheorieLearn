import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = r"$$\{0^p1^q0^r \mid r = p + q\}$$"

    server_base.generate(data)
