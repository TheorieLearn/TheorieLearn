from collections.abc import Callable
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    TypedDict,
    TypeVar,
)

from lxml.html import HtmlElement
from typing_extensions import NotRequired

class PartialScore(TypedDict):
    "A class with type signatures for the partial scores dict"

    score: float | None
    weight: NotRequired[int]
    feedback: NotRequired[str | dict[str, str] | Any]

class QuestionData(TypedDict):
    "A class with type signatures for the data dictionary"

    ai_grading: bool
    answers_names: dict[str, bool]
    correct_answers: dict[str, Any]
    editable: bool
    extensions: dict[str, Any]
    feedback: dict[str, Any]
    format_errors: dict[str, Any]
    manual_grading: bool
    num_valid_submissions: int
    options: dict[str, Any]
    panel: Literal["question", "submission", "answer"]
    params: dict[str, Any]
    partial_scores: dict[str, PartialScore]
    raw_submitted_answers: dict[str, Any]
    score: float
    submitted_answers: dict[str, Any]
    variant_seed: int

EnumT = TypeVar("EnumT", bound=Enum)

def get_boolean_attrib(
    element: HtmlElement, name: str, default: bool = False
) -> bool: ...
def get_integer_attrib(element: HtmlElement, name: str, default: int = 0) -> int: ...
def get_string_attrib(element: HtmlElement, name: str, default: str = "") -> str: ...
def get_float_attrib(
    element: HtmlElement, name: str, default: float = 0.0
) -> float: ...
def get_enum_attrib(
    element: HtmlElement, name: str, enum: Type[EnumT], default: Optional[EnumT] = None
) -> EnumT: ...
def has_attrib(element: HtmlElement, name: str) -> bool: ...
def index2key(i: int) -> str: ...
def get_uuid() -> str: ...
def inner_html(element: HtmlElement) -> str: ...
def to_json(v: Any) -> Dict[str, Any]: ...
def from_json(v: Dict[str, Any]) -> Any: ...
def check_attribs(
    element: HtmlElement, required_attribs: List[str], optional_attribs: List[str]
) -> None: ...
def escape_unicode_string(string: str) -> str: ...
def add_files_format_error(data: QuestionData, error: str) -> None: ...
def add_submitted_file(
    data: QuestionData,
    file_name: str,
    base64_contents: str | None = None,
    *,
    raw_contents: str | bytes | bytearray | None = None,
    mimetype: str | None = None,
) -> None: ...
def set_weighted_score_data(data: QuestionData, weight_default: int = 1) -> None: ...
def set_all_or_nothing_score_data(data: QuestionData) -> None: ...
def all_partial_scores_correct(data: QuestionData) -> bool: ...
def grade_answer_parameterized(
    data: QuestionData,
    name: str,
    grade_function: Callable[[Any], tuple[bool | float, str | None]],
    weight: int = 1,
) -> None: ...
