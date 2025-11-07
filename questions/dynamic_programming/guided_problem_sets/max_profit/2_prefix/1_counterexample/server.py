from typing import Any, Dict


def generate(data: Dict[str, Dict[str, Any]]) -> None:
    data["params"]["row_data"] = [
        {"i": 1},
        {"i": 2},
        {"i": 3},
        {"i": 4},
        {"i": 5},
        {"i": 6},
    ]
    maxprofit_subdef_correct = [5, 90, 90, 90, 107, 110]
    j_algorithm_correct = [0, 0, 1, 1, 3, 3]
    maxprofit_algorithm_correct = [5, 90, 90, 90, 190, 190]
    for i in range(1, 7):
        data["correct_answers"][f"maxprofit_{i}_subdef"] = maxprofit_subdef_correct[
            i - 1
        ]
        data["correct_answers"][f"j_{i}_algorithm"] = j_algorithm_correct[i - 1]
        data["correct_answers"][f"maxprofit_{i}_algorithm"] = (
            maxprofit_algorithm_correct[i - 1]
        )
