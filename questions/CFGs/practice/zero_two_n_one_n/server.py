import random
from typing import Any, Dict

import prairielearn as pl
import theorielearn.cfg_drill.server_base as server_base


def generate(data: Dict[str, Any]) -> None:
    block_length = random.randint(1, 4)
    data["params"]["target_string"] = "0" * 2 * block_length + "1" * block_length
    data["params"]["production_rules"] = ["S -> 00S1 | e"]

    server_base.generate(data)


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data)
