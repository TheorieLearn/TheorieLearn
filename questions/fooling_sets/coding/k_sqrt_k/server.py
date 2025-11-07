import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"$$L = \{w \mid |w| = \lceil  k\sqrt{k}\rceil, k\text{ is a natural number}\}$$. (Hint: Since this one is more difficult, try $$F = \{0^{m^6} \mid m \geq 1\}$$.)"
    )

    server_base.generate(data)
