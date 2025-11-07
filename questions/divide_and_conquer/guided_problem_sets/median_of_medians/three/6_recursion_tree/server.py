import theorielearn.recursion_tree.server_base as server_base
from theorielearn.shared_utils import QuestionData
from sympy import Rational


def generate(data: QuestionData) -> None:
    # In the format A(n/B) + C(n/D) + O(n^E)
    A = 1
    B = 3
    C = 1
    D = Rational(3, 2)
    E = 1

    server_base.generate(data, A, B, C, D, E)


def grade(data: QuestionData) -> None:
    server_base.grade(data)
