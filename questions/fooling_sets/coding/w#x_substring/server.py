import theorielearn.fooling_sets.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = (
        r"Strings of the form $$w\#x$$ where $$w$$ and $$x$$ are in $$\{0, 1\}^{*}$$ and $$w$$ is a substring of $$x$$."
    )

    server_base.generate(data)
