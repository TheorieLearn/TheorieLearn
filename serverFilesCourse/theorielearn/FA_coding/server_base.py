import chevron
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["names_for_user"] = []

    data["params"]["names_from_user"] = [
        {"name": "fa", "type": "either a DFA or NFA"},
    ]

    with open(
        data["options"]["server_files_course_path"]
        + "/theorielearn/FA_coding/question_base.mustache"
    ) as f:
        data["params"]["html"] = chevron.render(f, data["params"]).strip()
