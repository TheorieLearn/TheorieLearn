import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"$$L = \{ 0^i 1 0^j \mid \text{$i$ is divisible by $j$} \}$$"
    )

    server_base.generate(data)
