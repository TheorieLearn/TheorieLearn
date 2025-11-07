import random

import theorielearn.recursion_tree.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    # In the format A(n/B) + C(n/D) + O(n^E)

    B = random.randint(2, 5)
    C = 0
    D = 1
    E = random.randint(2, 3)
    A = B**E

    server_base.generate(data, A, B, C, D, E)


def grade(data: QuestionData) -> None:
    server_base.grade(data)
