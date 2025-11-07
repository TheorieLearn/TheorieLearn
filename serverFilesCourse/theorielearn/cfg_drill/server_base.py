from typing import Any, Dict

import chevron
import prairielearn as pl
from nltk.grammar import CFG
from theorielearn.shared_utils import grade_question_parameterized

import theorielearn.cfg_drill.utils as utils


def generate(data: Dict[str, Any]) -> None:
    data["params"]["latex_rules"] = utils.convert_production_rules_to_latex(
        data["params"]["production_rules"]
    )
    data["params"]["nltk_rules"] = utils.convert_production_rules_to_nltk(
        data["params"]["production_rules"]
    )
    with open(
        data["options"]["server_files_course_path"] + "/theorielearn/cfg_drill/question_base.html"
    ) as f:
        data["params"]["html"] = chevron.render(f, data).strip()


def grade(data: pl.QuestionData) -> None:
    data["submitted_answers"]["submission"] = utils.preprocess_submission(
        data["submitted_answers"]["_files"][0]["contents"]
    )

    grade_question_parameterized(
        data,
        "submission",
        lambda x: utils.check_submission(
            x,
            CFG.fromstring(data["params"]["nltk_rules"]),
            data["params"]["target_string"],
        ),
    )

    pl.set_weighted_score_data(data)
