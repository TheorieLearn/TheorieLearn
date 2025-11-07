import prairielearn as pl
import theorielearn.shared_utils as su


def grade(data: su.QuestionData) -> None:
    def grade_q3(student_ans: str) -> tuple[bool, str | None]:
        if student_ans == "Bellman Ford&#x27;s Algorithm":
            return (
                False,
                "Is Bellman Ford's algorithm the fastest algorithm to solve this problem?",
            )
        if student_ans == "Dijkstra&#x27;s Algorithm":
            return (
                False,
                "Is Dijkstra's algorithm the fastest algorithm to solve this problem?",
            )
        if student_ans == "Kosaraju-Sharir&#x27;s Algorithm":
            return False, "Does Kosaraju-Sharir's algorithm solve the problem?"
        return True, None

    su.grade_question_parameterized(data, "q3", grade_q3)
    pl.set_weighted_score_data(data)
