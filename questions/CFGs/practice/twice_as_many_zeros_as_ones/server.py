import random
from typing import Any, Dict

from prairielearn import QuestionData
import theorielearn.cfg_drill.server_base as server_base


def generate(data: Dict[str, Any]) -> None:
    target_string = ["0"] * 6 + ["1"] * 3
    random.shuffle(target_string)
    data["params"]["target_string"] = "".join(target_string)
    data["params"]["production_rules"] = ["S -> e | SS | 00S1 | 0S1S0 | 1S00"]
    server_base.generate(data)


def grade(data: QuestionData) -> None:
    server_base.grade(data)
