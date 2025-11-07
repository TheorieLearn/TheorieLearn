import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = r"$$\{0^i1^j2^k \mid i+j = k + 1\}$$"

    server_base.generate(data)
