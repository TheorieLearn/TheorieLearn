import json
from enum import Enum

import chevron
import lxml.html
import prairielearn as pl
from typing_extensions import Optional

TREE_BUILDER_MUSTACHE_TEMPLATE_NAME = "tl-tree-builder.mustache"


class Mode(Enum):
    BUILDER = "builder"
    POINTER = "pointer"
    POINTER_DELETE = "pointer-delete"
    RECURRENCE = "recurrence"
    VALUE = "value"
    VIEW_ONLY = "view-only"
    SIDE_LABEL = "side-label"
    ANIMATION = "animation"
    FEEDBACK_ANIMATION = "feedback-animation"


class NodeDrawMode(Enum):
    CIRCLE = "circle"
    SQUARE = "square"
    TRIANGLE = "triangle"


class ElementSize(Enum):
    NORMAL = "normal"
    SMALL = "small"


def prepare(element_html: str, data: pl.QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)
    required_attribs = ["answers-name"]
    optional_attribs = ["mode", "node_draw_mode", "size"]
    pl.check_attribs(element, required_attribs, optional_attribs)

    name = pl.get_string_attrib(element, "answers-name")

    data["params"][name] = dict()


def render(element_html: str, data: pl.QuestionData) -> str:
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, "answers-name")
    mode = pl.get_enum_attrib(element, "mode", Mode, Mode.BUILDER)
    node_draw_mode = pl.get_enum_attrib(
        element, "node_draw_mode", NodeDrawMode, NodeDrawMode.CIRCLE
    )
    shrink_tree = (
        pl.get_enum_attrib(element, "size", ElementSize, ElementSize.NORMAL)
        == ElementSize.SMALL
    )

    # Takes the submitted student answer to rerender the same tree so nothing disappears.
    # If nothing has been submitted, populates with the start-tree given in question params, if exists.
    startertree = data["params"].get(
        name + "start-tree", data["params"].get("start-tree", None)
    )

    treeframes = data["params"].get(
        name + "tree-frames", data["params"].get("tree-frames", [])
    )
    if len(treeframes) > 0 and mode in (Mode.ANIMATION, Mode.FEEDBACK_ANIMATION):
        startertree = treeframes[0]

    # Hack so you can have two separate tree builder elements, one displaying the start tree, one display the answer
    # The one displaying the answer must have the param 'answer-name' set to "DEBUG_DISPLAY_ANSWER"
    if name == "DEBUG_DISPLAY_ANSWER":
        startertree = data["params"].get("tree", startertree)
    treejson = data["submitted_answers"].get(name, startertree)
    labeltreejson = data["params"].get(
        name + "node-tree", data["params"].get("node-tree", startertree)
    )
    sidetreejson = startsidetreejson = data["params"].get("start-side-tree", [])
    height_text = ""
    leaf_count_text = ""

    # Okay so this is super hacky, but if there's a starter tree treejson will equal that, but won't be in
    # the double submission format we have for recurrences, so we have to make sure there was an actual submission first.
    # before loading it in. This is mostly so the interface persists after pressing submit.
    if (
        mode is Mode.RECURRENCE
        and name in data["submitted_answers"]
        and treejson is not None
    ):
        sidetreejson = treejson["WorkPerLevel"]
        height_text = treejson["Height"]
        leaf_count_text = treejson["LeafCount"]
        treejson = treejson["WorkPerCall"]

    leaf_value_text = data["params"].get("leaf-value", "")

    fix_node_height = data["params"].get("fix_node_height", False)

    editable = data["editable"]
    mode_toggle = data["params"].get("mode_toggle", False)
    enable_height = data["params"].get("enable_height", False)

    enable_subtrees = data["params"].get("enable_subtrees", True)

    # This is entirely to move some of the frontend data from parse to render, because when a student submits
    # in the middle of editing a tree that is now in an illegal state, it undos to the last legal state,
    # and it would be distressing to see an error message without being able to see the error
    frontenddata = data["submitted_answers"].get(
        name + "raw-student-frontend-for-visual", None
    )
    # This is to move the students current edit mode, when they are toggling modes,
    #  from the submitted answers to the new render, so it doesn't try to switch modes on the student
    # Which would cause issues if pointer mode is in an error state and then tries to render in builder mode
    # Defaults to the provided mode if there is no submission or if mode_toggle is False
    mode = (
        mode
        if not mode_toggle
        else Mode(
            data["submitted_answers"].get(name + "student-current-mode", mode.value)
        )
    )

    feedback_canvas = mode is Mode.FEEDBACK_ANIMATION
    mode = Mode.ANIMATION if mode is Mode.FEEDBACK_ANIMATION else mode

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
            "tree_frames": treeframes,
            "tree_frame_inds": list(range(len(treeframes))),
            "fix_node_height": fix_node_height,
            "editable": editable and mode != Mode.ANIMATION,
            "builder_instructions": (mode is Mode.BUILDER or mode_toggle),
            "pointer_instructions": (mode is Mode.POINTER or mode_toggle),
            "side_label_instructions": (mode is Mode.SIDE_LABEL),
            "recurrence_instructions": (mode is Mode.RECURRENCE),
            "pointer_delete_instructions": (mode is Mode.POINTER_DELETE),
            "value_only_instructions": mode is Mode.VALUE,
            "animation_mode": mode is Mode.ANIMATION,
            "mode": mode.value,
            "front_end_data": frontenddata,
            "numeric_only": data["params"].get("numeric_only", False),
            "submission": (data["panel"] == "submission"),
            "parse_errors": data["format_errors"].get(name, None),
            "side-tree-json": sidetreejson,
            "starter-side-tree-json": startsidetreejson,
            # Mustache doesn't handle empty lists well, this is to compensate
            "bool-side-json": bool(len(sidetreejson)),
            "enable-final-level": data["params"].get("enable-final-level", False),
            "bool-start-side": bool(len(startsidetreejson)),
            "leaf-count": leaf_count_text,
            "leaf-value": leaf_value_text,
            "feedback": (
                partial_scores.get("feedback", None) if partial_scores else None
            ),
            "node_draw_mode": node_draw_mode.value,
            "mode_toggle": mode_toggle,
            "enable-subtree": enable_subtrees,
            "enable-height": enable_height,
            "height_init": height_text,
            "height_limit": data["params"].get("levels_graded", -1),
            "shrink_tree": shrink_tree,
            "toggle_small": shrink_tree or data["params"].get("small_nodes", False),
            "interval": data["params"].get("animation-interval", 1000),
            "feedback-canvas": feedback_canvas,
            "label_tree_json": labeltreejson,
        }

        with open(TREE_BUILDER_MUSTACHE_TEMPLATE_NAME, "r") as f:
            return chevron.render(f, html_params).strip()


def parse(element_html: str, data: pl.QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, "answers-name")
    startmode = pl.get_enum_attrib(element, "mode", Mode, Mode.BUILDER)

    if startmode in (Mode.VIEW_ONLY, Mode.ANIMATION, Mode.FEEDBACK_ANIMATION):
        return

    try:
        tree_json = json.loads(data["raw_submitted_answers"][name + "-raw"])
    except Exception:
        print(data["raw_submitted_answers"][name + "-raw"])
        data["format_errors"][name] = {"message": f"Invalid JSON for {name}"}
        return

    if tree_json["format-errors"] != "":
        data["format_errors"][name] = {"message": tree_json["format-errors"]}
        # If we're in pointer mode this will redraw the tree properly:
        frontendtree = tree_json["frontend"]
        data["submitted_answers"][name + "raw-student-frontend-for-visual"] = (
            frontendtree
        )
    # For when we have to toggle modes then redisplay:
    data["submitted_answers"][name + "student-current-mode"] = tree_json["currentMode"]

    backendtree = tree_json["backendRoot"]

    if backendtree is None:
        data["format_errors"][name] = {"message": "Empty tree"}
        return

    if startmode is Mode.RECURRENCE:
        data["submitted_answers"][name] = {
            "WorkPerCall": backendtree,
            "WorkPerLevel": tree_json["sideTree"],
            "Height": tree_json["height-val"],
            "LeafCount": tree_json["leaf-count"],
        }
    else:
        data["submitted_answers"][name] = backendtree
