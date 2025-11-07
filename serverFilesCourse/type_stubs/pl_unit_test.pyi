from collections import namedtuple
from types import ModuleType
from typing import Any
import prairielearn as pl
import unittest

class PLTestCase(unittest.TestCase):
    include_plt: bool
    student_code_file: str
    iter_num: int
    total_iters: int
    ipynb_key: str
    plt: ModuleType | None

    data: pl.QuestionData
    # These are named tuples for reference and student results
    ref: Any
    st: Any

    @classmethod
    def setUpClass(cls) -> None: ...
    @classmethod
    def tearDownClass(cls) -> None: ...
    @classmethod
    def display_plot(cls) -> None: ...
    @classmethod
    def get_total_points(cls) -> float: ...
    def setUp(self) -> None: ...
    def run(self, result: unittest.TestResult | None = None) -> None: ...
