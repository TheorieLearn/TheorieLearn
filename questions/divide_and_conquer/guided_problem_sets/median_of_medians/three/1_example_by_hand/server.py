from typing import Any, Dict

import numpy as np


def generate(data: Dict[str, Any]) -> None:
    A = np.random.permutation(90)[:21].reshape(-1, 3) + 10
    data["params"]["input_array"] = ",\n  ".join(
        ",  ".join(str(elem) for elem in row) for row in A
    )

    medians = np.median(A, axis=1).astype(int)
    data["correct_answers"]["A1"] = "[" + ",".join(str(i) for i in medians) + "]"
    data["correct_answers"]["k1"] = 4

    pivot = np.median(medians).astype(int)

    k_low = np.random.randint(2, 5)
    k_high = np.random.randint(17, 20)

    data["params"]["k_low"] = k_low
    data["params"]["k_high"] = k_high

    A = A.flatten()  # partition is determined

    data["correct_answers"]["A_low"] = (
        "[" + ",".join(str(i) for i in A if i < pivot) + "]"
    )
    data["correct_answers"]["A_high"] = (
        "[" + ",".join(str(i) for i in A if i > pivot) + "]"
    )
    data["correct_answers"]["k_low"] = k_low
    data["correct_answers"]["k_high"] = int(k_high - sum(i <= pivot for i in A))
