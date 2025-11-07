import random
from typing import Any, Dict, List

from prairielearn import QuestionData
import theorielearn.cfg_drill.server_base as server_base


def generate(data: Dict[str, Any]) -> None:
    target_string: List[str] = []
    while len(target_string) == 0 or (
        len(target_string) % 2 == 0
        and target_string[: len(target_string) // 2]
        == target_string[len(target_string) // 2 :]
    ):
        target_string = ["0"] * random.randint(2, 5) + ["1"] * random.randint(2, 5)
        random.shuffle(target_string)
    data["params"]["target_string"] = "".join(target_string)
    data["params"]["production_rules"] = [
        "S -> AB | BA | A | B",
        "A -> 0 | 0A0 | 0A1 | 1A0 | 1A1",
        "B -> 1 | 0B0 | 0B1 | 1B0 | 1B1",
    ]

    server_base.generate(data)


def grade(data: QuestionData) -> None:
    server_base.grade(data)
