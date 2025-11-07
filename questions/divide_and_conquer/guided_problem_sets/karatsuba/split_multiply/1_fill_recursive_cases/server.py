import random
from typing import Any, Dict

from theorielearn.shared_utils import integer_is_outside_PL_limit


def generate(data: Dict[str, Any]) -> None:
    have_generated_answers = False
    while not have_generated_answers:
        m = 4
        first_number = random.randint(10 ** (2 * m - 1), 10 ** (2 * m) - 1)
        second_number = random.randint(10 ** (2 * m - 1), 10 ** (2 * m) - 1)

        ten_power_m = 10**m
        a = first_number // ten_power_m
        b = first_number % ten_power_m
        c = second_number // ten_power_m
        d = second_number % ten_power_m
        e = a * c
        f = b * d
        g = b * c
        h = a * d

        data["params"]["first_number"] = first_number
        data["params"]["second_number"] = second_number
        data["params"]["e"] = e
        data["params"]["f"] = f
        data["params"]["g"] = g
        data["params"]["h"] = h

        data["params"]["m"] = m
        data["params"]["n"] = 2 * m
        data["params"]["ordinals"] = ["first", "second", "third", "fourth"]

        data["correct_answers"]["first_call_param_1"] = a
        data["correct_answers"]["first_call_param_2"] = c
        data["correct_answers"]["second_call_param_1"] = b
        data["correct_answers"]["second_call_param_2"] = d
        data["correct_answers"]["third_call_param_1"] = b
        data["correct_answers"]["third_call_param_2"] = c
        data["correct_answers"]["fourth_call_param_1"] = a
        data["correct_answers"]["fourth_call_param_2"] = d

        data["correct_answers"]["first_summand"] = ten_power_m**2 * e
        data["correct_answers"]["second_summand"] = ten_power_m * (g + h)
        data["correct_answers"]["third_summand"] = f

        if not integer_is_outside_PL_limit(ten_power_m**2 * e):
            have_generated_answers = True
