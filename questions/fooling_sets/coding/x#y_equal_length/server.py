import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"Strings of the form $$x\#y$$ where $$x$$ and $$y$$ are strings of the same length in $$\{0, 1\}^{*}$$."
    )

    server_base.generate(data)
