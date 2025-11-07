import random
import re
from typing import Any, Dict

import prairielearn as pl
import theorielearn.fooling_set_drill.server_base as server_base


def has_correct_counts(result: str) -> bool:
    for i in range(0, len(result), 2):
        if result == "01" * (i // 2) + "10" * ((len(result) - i) // 2):
            return i == len(result) - i

    return len(result) == 0


def grade(data: pl.QuestionData) -> None:
    server_base.grade(
        data,
        lambda x: (re.fullmatch("(01)*(10)*", x) is not None) and has_correct_counts(x),
    )


def generate(data: Dict[str, Any]) -> None:
    data["params"]["non_regular_language"] = r"\{(01)^{n}(10)^{n} \mid n \geq 0\}"
    data["params"]["fooling_set"] = "(01)^{*}"
    [fooling_set_member_1, fooling_set_member_2] = random.sample(
        ["01" * n for n in range(4)], 2
    )
    data["params"]["fooling_set_member_1_display"] = (
        fooling_set_member_1 if len(fooling_set_member_1) != 0 else r"\varepsilon"
    )
    data["params"]["fooling_set_member_2_display"] = (
        fooling_set_member_2 if len(fooling_set_member_2) != 0 else r"\varepsilon"
    )
    data["params"]["fooling_set_member_1"], data["params"]["fooling_set_member_2"] = (
        fooling_set_member_1,
        fooling_set_member_2,
    )

    server_base.generate(data)
