import random
from typing import Any, Dict

import prairielearn as pl
import theorielearn.fooling_set_drill.server_base as server_base
from theorielearn.shared_utils import is_perfect_power


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data, lambda x: is_perfect_power(len(x), 3) and x == "0" * len(x))


def generate(data: Dict[str, Any]) -> None:
    data["params"]["non_regular_language"] = r"\{0^{n^{3}} \mid n \geq 0\}"
    data["params"]["fooling_set"] = r"\{0^{n^{3}} \mid n \geq 0\}"
    [fooling_set_member_1, fooling_set_member_2] = random.sample(
        ["0" * (n**3) for n in range(10)], 2
    )
    data["params"]["fooling_set_member_1_display"] = (
        f"0^{{{str(len(fooling_set_member_1))}}}"
        if len(fooling_set_member_1) != 0
        else r"\varepsilon"
    )
    data["params"]["fooling_set_member_2_display"] = (
        f"0^{{{str(len(fooling_set_member_2))}}}"
        if len(fooling_set_member_2) != 0
        else r"\varepsilon"
    )
    data["params"]["fooling_set_member_1"], data["params"]["fooling_set_member_2"] = (
        fooling_set_member_1,
        fooling_set_member_2,
    )

    server_base.generate(data)
