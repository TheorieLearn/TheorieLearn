import random
from typing import Any, Dict


def generate(data: Dict[str, Any]) -> None:
    data["params"]["num0s"] = num0s = random.randint(5, 20)
    data["params"]["num01s"] = num01s = random.randint(5, 20)

    data["correct_answers"]["0-transition-num0s"] = num0s + 1
    data["correct_answers"]["0-transition-num01s"] = num01s
    data["correct_answers"]["1-transition-num0s"] = num0s
    data["correct_answers"]["1-transition-num01s"] = num0s + num01s
