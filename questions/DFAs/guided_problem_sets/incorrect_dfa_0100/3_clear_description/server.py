from typing import Any, Dict

from theorielearn.FA_coding.incorrect_dfa_for_0100 import fa as dfa


def generate(data: Dict[str, Any]) -> None:
    data["params"]["dfa"] = dfa.show_diagram().string()
