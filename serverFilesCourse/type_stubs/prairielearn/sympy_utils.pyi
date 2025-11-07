from collections.abc import Callable
from typing import Any, Literal, TypedDict
import sympy
from dataclasses import dataclass
from typing_extensions import NotRequired

SympyMapT = dict[str, sympy.Basic | complex]
SympyFunctionMapT = dict[str, Callable[..., Any]]
AssumptionsDictT = dict[str, dict[str, Any]]

class SympyJson(TypedDict):
    """A class with type signatures for the SymPy JSON dict"""

    _type: Literal["sympy"]
    _value: str
    _variables: list[str]
    _assumptions: NotRequired[AssumptionsDictT]
    _custom_functions: NotRequired[list[str]]


class LocalsForEval(TypedDict):
    """A class with type signatures for the locals_for_eval dict"""

    functions: SympyFunctionMapT
    variables: SympyMapT
    helpers: SympyFunctionMapT

def evaluate(
    expr: str, locals_for_eval: LocalsForEval, *, allow_complex: bool = False
) -> sympy.Expr: ...

class BaseSympyError(Exception):
    """Exception base class for SymPy parsing errors"""

@dataclass
class HasInvalidFunctionError(BaseSympyError):
    offset: int
    text: str

@dataclass
class HasInvalidVariableError(BaseSympyError):
    offset: int
    text: str

@dataclass
class HasEscapeError(BaseSympyError):
    offset: int

@dataclass
class HasCommentError(BaseSympyError):
    offset: int

def json_to_sympy(
    sympy_expr_dict: SympyJson,
    *,
    allow_complex: bool = True,
    allow_trig_functions: bool = True,
    simplify_expression: bool = True,
) -> sympy.Expr: ...
