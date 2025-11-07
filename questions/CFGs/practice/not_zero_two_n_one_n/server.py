import random
import re
from typing import Any, Dict

from prairielearn import QuestionData
import theorielearn.cfg_drill.server_base as server_base


def generate(data: Dict[str, Any]) -> None:
    target_string = ""
    pattern = re.compile("0*1*")
    while target_string.count("0") == 2 * target_string.count("1") and re.fullmatch(
        pattern, target_string
    ):
        target_string = "".join(
            str(random.randint(0, 1)) for _ in range(random.randint(4, 6))
        )

    data["params"]["target_string"] = target_string
    data["params"]["production_rules"] = [
        "S -> T | X",
        "T -> 00T1 | A | B | C",
        "A -> 0 | 0A",
        "B -> 1 | 1B",
        "C -> 0 | 0B",
        "X -> Z10Z",
        "Z -> e | 0Z | 1Z",
    ]

    server_base.generate(data)


def grade(data: QuestionData) -> None:
    server_base.grade(data)
