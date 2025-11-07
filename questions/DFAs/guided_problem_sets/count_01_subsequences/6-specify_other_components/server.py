import base64
from typing import Any, Dict, Optional


def generate(data: Dict[str, Any]) -> None:
    data["params"]["names_for_user"] = []
    data["params"]["names_from_user"] = [
        {"name": "start_state"},
        {"name": "transition0"},
        {"name": "transition1"},
        {"name": "accept_condition"},
    ]


def base64_encode_string(string: str) -> str:
    # do some wonky encode/decode because base64 expects a bytes object
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")


def pythonize_math_expression(string: Optional[str]) -> str:
    if string is None:
        return ""
    return string.replace(" mod ", " % ").replace("==", "=").replace("=", "==")


def parse(data: Dict[str, Any]) -> None:
    submitted_answers = data["submitted_answers"]
    code = f"""
start_state = {submitted_answers["start_state"]}
transition0 = lambda num0s, num01s: {pythonize_math_expression(submitted_answers["transition0"])}
transition1 = lambda num0s, num01s: {pythonize_math_expression(submitted_answers["transition1"])}
accept_condition = lambda num0s, num01s: {pythonize_math_expression(submitted_answers["accept_condition"])}
"""

    # ship the answer off to the autograder
    data["submitted_answers"]["_files"] = [
        {"name": "user_code.py", "contents": base64_encode_string(code)}
    ]
