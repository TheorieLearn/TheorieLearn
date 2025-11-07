import random
import re
from typing import Any, Dict

import prairielearn as pl
import theorielearn.fooling_set_drill.server_base as server_base


def grade(data: pl.QuestionData) -> None:
    server_base.grade(
        data,
        lambda x: (x.count("0") != 2 * x.count("1"))
        and (re.fullmatch("0*1*", x) is not None),
    )


def generate(data: Dict[str, Any]) -> None:
    data["params"]["non_regular_language"] = r"\{0^{m}1^{n} \mid m \neq 2n\}"
    data["params"]["fooling_set"] = "0^{*}"
    [fooling_set_member_1, fooling_set_member_2] = random.sample(
        ["0" * n for n in range(10)], 2
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
