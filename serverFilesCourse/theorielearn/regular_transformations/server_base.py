import chevron
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["names_for_user"] = []

    data["params"]["names_from_user"] = [
        {"name": "transform", "type": "function returning a DFA or NFA"},
    ]

    with open(
        data["options"]["server_files_course_path"]
        + "/theorielearn/regular_transformations/question_base.html"
    ) as f:
        data["params"]["html"] = chevron.render(f, data["params"]).strip()
