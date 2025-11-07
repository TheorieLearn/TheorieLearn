import random
from typing import Any, Dict


def get_random_string() -> str:
    return "".join(random.choice("01") for _ in range(9))


def count_01_subsequences(string: str) -> int:
    num0s = 0
    num01s = 0
    for c in string:
        if c == "0":
            num0s += 1
        else:
            num01s += num0s
    return num01s


def generate(data: Dict[str, Any]) -> None:
    string_in_L = get_random_string()
    while count_01_subsequences(string_in_L) % 7 != 4:
        string_in_L = get_random_string()

    string_notin_L = get_random_string()
    while count_01_subsequences(string_notin_L) % 7 == 4:
        string_notin_L = get_random_string()

    data["params"]["string_in_L"] = string_in_L
    data["params"]["string_notin_L"] = string_notin_L

    data["correct_answers"]["num_01_in"] = count_01_subsequences(string_in_L)
    data["correct_answers"]["num_01_notin"] = count_01_subsequences(string_notin_L)
