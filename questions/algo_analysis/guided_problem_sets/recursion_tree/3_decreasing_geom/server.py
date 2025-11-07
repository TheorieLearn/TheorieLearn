import random

import theorielearn.recursion_tree.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    # In the format A(n/B) + C(n/D) + O(n^E)
    D = random.randint(2, 4)
    B = random.randint(D + 1, D + 2)
    E = random.randint(2, 3)
    A = random.randint(1, B)
    C = random.randint(1, D)

    server_base.generate(data, A, B, C, D, E)


def grade(data: QuestionData) -> None:
    server_base.grade(data)
