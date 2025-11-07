from typing import Callable, Generic, List, Optional, Tuple, Type, TypeVar

from theorielearn.shared_utils import QuestionData, grade_question_parameterized

from theorielearn.scaffolded_writing.cfg import ScaffoldedWritingCFG
from theorielearn.scaffolded_writing.student_submission import StudentSubmission

SubmissionT = TypeVar("SubmissionT", bound=StudentSubmission)
ConstraintFunctionT = Callable[[SubmissionT], Optional[str]]


class IncrementalConstraintGrader(Generic[SubmissionT]):
    "Class for incrementally constructing a grader for scaffolded writing questions"

    constraints: List[Tuple[ConstraintFunctionT, float]]
    submission_type: Type[SubmissionT]
    question_cfg: ScaffoldedWritingCFG

    def __init__(
        self, submission_type: Type[SubmissionT], question_cfg: ScaffoldedWritingCFG
    ) -> None:
        if not issubclass(submission_type, StudentSubmission):
            raise TypeError(
                f"Submission type {submission_type} is not a subclass of StudentSubmission"
            )
        self.submission_type = submission_type
        self.question_cfg = question_cfg
        self.constraints = []

    def add_constraint(
        self, constraint: ConstraintFunctionT, partial_credit: float = 1.0
    ) -> None:
        "Add constraint to use for grading, granting partial_credit if the constraint is satisfied"
        if not 0.0 < partial_credit <= 1.0:
            raise ValueError(
                f"The value {partial_credit} given for partial credit is not in (0,1]"
            )
        elif len(self.constraints) > 0 and self.constraints[-1][1] > partial_credit:
            raise ValueError("New partial credit value not increasing")

        self.constraints.append((constraint, partial_credit))

    def grade_question(self, data: QuestionData, question_name: str) -> None:
        "Grade question_name using the constraints in the given list"
        if len(self.constraints) == 0:
            raise ValueError("No constraints set for this grader")
        elif self.constraints[-1][1] != 1.0:
            raise ValueError("Final constraint in grader doesn't grant full credit")

        def constraint_grader(tokens: List[str]) -> Tuple[float, Optional[str]]:
            submission = self.submission_type(tokens, self.question_cfg)

            prev_score = 0.0
            for constraint, partial_credit in self.constraints:
                feedback = constraint(submission)
                if feedback is not None:
                    return prev_score, feedback

                prev_score = partial_credit

            return prev_score, None

        grade_question_parameterized(data, question_name, constraint_grader)
