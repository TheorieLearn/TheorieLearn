import json

import chevron
import lxml.html
import prairielearn as pl
from typing_extensions import Optional

BTREE_BUILDER_MUSTACHE_TEMPLATE_NAME = "tl-btree-builder.mustache"


def prepare(element_html: str, data: pl.QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)
    required_attribs = ["answers-name"]
    optional_attribs: list[str] = []
    pl.check_attribs(element, required_attribs, optional_attribs)

    name = pl.get_string_attrib(element, "answers-name")

    data["params"][name] = dict()


def render(element_html: str, data: pl.QuestionData) -> str:
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, "answers-name")

    # Takes the submitted student answer to rerender the same tree so nothing disappears.
    # If nothing has been submitted, populates with the start-tree given in question params, if exists.
    startertree = data["params"].get("start-tree", None)
    treejson = data["submitted_answers"].get(name, startertree)

    editable = data["params"].get("editable", True)

    if data["panel"] == "answer":
        return ""
    else:
        partial_scores: Optional[pl.PartialScore] = data["partial_scores"].get(
            name, None
        )
        html_params = {
            "question": (data["panel"] == "question"),
            "answers_name": name,
            "tree_json": treejson,
            "starttree_json": startertree,
            "editable": editable,
            "small_nodes": data["params"].get("small_nodes", False),
            "numeric_only": data["params"].get("numeric_only", False),
            "submission": (data["panel"] == "submission"),
            "parse_errors": data["format_errors"].get(name, None),
            "feedback": (
                partial_scores.get("feedback", None) if partial_scores else None
            ),
        }

        with open(BTREE_BUILDER_MUSTACHE_TEMPLATE_NAME, "r") as f:
            return chevron.render(f, html_params).strip()


def parse(element_html: str, data: pl.QuestionData) -> None:
    if not data["params"].get("editable", True):
        return

    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, "answers-name")
    try:
        tree_json = json.loads(data["raw_submitted_answers"][name + "-raw"])
    except Exception:
        data["format_errors"][name] = {"message": f"Invalid JSON for {name}"}
        return

    backendtree = tree_json["backendRoot"]

    if backendtree is None:
        data["format_errors"][name] = {"message": "Empty tree"}
        return

    data["submitted_answers"][name] = backendtree
