import random

from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    # Generate two two-digit numbers to add mod 10 that goes into negative
    zero_left = random.randint(10, 29)
    zero_right = random.randint(-99, -30)
    zero_mod = random.randint(3, 9)

    data["params"]["zero_left"] = zero_left
    data["params"]["zero_right"] = zero_right
    data["params"]["zero_mod"] = zero_mod

    # Generate two two-digit numbers to add mod 10
    one_left = random.randint(10, 99)
    one_right = random.randint(10, 99)
    one_mod = random.randint(3, 9)

    data["params"]["one_left"] = one_left
    data["params"]["one_right"] = one_right
    data["params"]["one_mod"] = one_mod

    # Generate two medium sized numbers to multiply mod something one less
    two_left = random.randint(10, 99)
    two_right = random.randint(10, 99)
    two_mod = two_left - 1

    data["params"]["two_left"] = two_left
    data["params"]["two_right"] = two_right
    data["params"]["two_mod"] = two_mod

    # Generate two medium sized numbers to multiply mod something one more
    three_left = random.randint(10, 99)
    three_right = random.randint(10, 99)
    three_mod = three_right + 1

    data["params"]["three_left"] = three_left
    data["params"]["three_right"] = three_right
    data["params"]["three_mod"] = three_mod

    # Put the sum into data['correct_answers']
    data["correct_answers"]["w"] = (zero_left + zero_right) % zero_mod
    data["correct_answers"]["x"] = (one_left + one_right) % one_mod
    data["correct_answers"]["y"] = (two_left * two_right) % two_mod
    data["correct_answers"]["z"] = (three_left * three_right) % three_mod
