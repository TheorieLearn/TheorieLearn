import random
from typing import Any, Dict

from prairielearn import QuestionData
import theorielearn.cfg_drill.server_base as server_base


def generate(data: Dict[str, Any]) -> None:
    n = random.randint(3, 5)
    m = random.choice([i for i in range(6, 10) if i != 2 * n])
    data["params"]["target_string"] = "0" * m + "1" * n
    data["params"]["production_rules"] = [
        "S -> M | L",
        "M -> 0M | 0E",
        "L -> L1 | E1",
        "E -> e | 0 | 00E1",
    ]

    server_base.generate(data)


def grade(data: QuestionData) -> None:
    server_base.grade(data)
