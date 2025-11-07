import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {
        "ValidShuffle": 2,
        "Or": 2,
        "Equals": 2,
        "And": 2,
        "A": 1,
        "B": 1,
        "C": 1,
    }
    local_variables = {"i", "j", "n", "and", "CaseA", "CaseB"}

    SympyGrader("ans1", local_functions, local_variables).grade_question(
        data, "ValidShuffle(i-1, j)"
    )

    SympyGrader("ans2", local_functions, local_variables).grade_question(
        data, "ValidShuffle(i, j-1)"
    )

    SympyGrader("ans3", local_functions, local_variables).grade_question(
        data,
        "And(Equals(A(i),C(i+j)), ValidShuffle(i-1, j))",
        "And(Equals(C(i+j), A(i)), ValidShuffle(i-1, j))",
        "And(ValidShuffle(i-1, j), Equals(A(i),C(i+j)))",
        "And(ValidShuffle(i-1, j), Equals(C(i+j),A(i)))",
    )

    SympyGrader("ans4", local_functions, local_variables).grade_question(
        data,
        "And(Equals(B(j),C(i+j)), ValidShuffle(i, j-1))",
        "And(Equals(C(i+j), B(i)), ValidShuffle(i, j-1))",
        "And(ValidShuffle(i, j-1), Equals(B(j),C(i+j)))",
        "And(ValidShuffle(i, j-1), Equals(C(i+j),B(j)))",
    )

    SympyGrader("final", local_functions, local_variables).grade_question(
        data, "Or(CaseA, CaseB)", "Or(CaseB, CaseA)"
    )

    pl.set_weighted_score_data(data)
