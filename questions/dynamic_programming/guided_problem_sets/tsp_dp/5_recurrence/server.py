import prairielearn as pl
from theorielearn.shared_utils import QuestionData
from theorielearn.sympy_utils.utils import SympyGrader


def grade(data: QuestionData) -> None:
    local_functions = {"WorldTour": 2, "d": 2}
    local_variables = {"i", "n", "t", "S", "R"}

    recursive_grader = SympyGrader("recursive", local_functions, local_variables)
    recursive_grader.answer_not_includes_function_feedback(
        "d",
        "You need to include the distance from $t$ to some other vertex"
        " in your recursive case.",
    )
    recursive_grader.answer_not_includes_function_feedback(
        "WorldTour",
        r"Your recursive case must recursively call the $\mathsf{WorldTour}$ function!",
    )
    recursive_grader.answer_function_with_argument_feedback(
        "WorldTour",
        "S",
        "You must remove something from the set $S$ before"
        r" recursively calling $\mathsf{WorldTour}$.",
    )
    recursive_grader.grade_question(
        data, "d(i,t) + WorldTour(S - t,t)", "d(t,i) + WorldTour(S - t,t)"
    )

    base_case_grader = SympyGrader("base_case1", local_functions, local_variables)
    base_case_grader.answer_includes_function_feedback(
        "WorldTour",
        r"Your base case must not recursively call the $\mathsf{WorldTour}$ function!",
    )
    base_case_grader.answer_not_includes_function_feedback(
        "d", r"Your base case should include the distance function $d$."
    )
    base_case_grader.answer_function_without_argument_feedback(
        "d",
        "0",
        "Remember that your base case should include the distance to Momo's home, city $0$.",
    )
    base_case_grader.grade_question(data, "d(i,0)", "d(0,i)")

    final_grader = SympyGrader("final", local_functions, local_variables)
    final_grader.answer_not_includes_function_feedback(
        "d", "Your answer should include the distance to Momo's home city, $0$."
    )
    final_grader.answer_function_without_argument_feedback(
        "d", "0", "Your answer should include the distance to Momo's home city, $0$."
    )
    final_grader.grade_question(
        data, "d(i,0) + WorldTour(R - i,i)", "d(0,i) + WorldTour(R - i,i)"
    )

    pl.set_weighted_score_data(data)
