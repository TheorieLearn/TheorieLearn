import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"L = $\{0^a 1 w 1 0^c \mid w \in \Sigma^{\ast}, (a \leq |w| + c) \text{ and } (|w| \leq a + c \text{ or } c \leq a + |w|) \}$, $\Sigma = \{0, 1\}$."
    )

    server_base.generate(data)
