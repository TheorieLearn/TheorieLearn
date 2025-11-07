import chevron
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["names_for_user"] = []

    data["params"]["names_from_user"] = [
        {"name": "getFoolingSetElement", "type": "function"},
        {"name": "getDistinguishingSuffix", "type": "function"},
    ]

    with open(
        data["options"]["server_files_course_path"] + "/theorielearn/fooling_sets/question_base.html"
    ) as f:
        data["params"]["html"] = chevron.render(f, data["params"]).strip()
