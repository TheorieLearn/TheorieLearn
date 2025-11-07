from collections.abc import Callable
from typing import Any, Literal, NoReturn, TypeVar

import numpy as np
from matplotlib.axes import Axes
from numpy.typing import ArrayLike, NDArray
from pandas import DataFrame

T = TypeVar("T")

class Feedback:
    test_name: str
    feedback_file: str
    prefix_message: str
    buffer: str

    @classmethod
    def set_name(cls, name: str) -> None: ...

    @classmethod
    def set_main_output(cls) -> None: ...

    @classmethod
    def set_test(cls, test: Any) -> None: ...

    @classmethod
    def set_score(cls, score: float) -> None: ...

    @classmethod
    def add_iteration_prefix(cls, iter_prefix: int) -> None: ...

    @classmethod
    def clear_iteration_prefix(cls) -> None: ...

    @classmethod
    def add_feedback(cls, text: str) -> None: ...

    @classmethod
    def finish(cls, fb_text: str) -> NoReturn: ...

    @classmethod
    def finish_test(cls, fb_text: str) -> NoReturn: ...

    @staticmethod
    def not_allowed(*_args: Any, **_kwargs: Any) -> NoReturn: ...

    @classmethod
    def check_numpy_array_sanity(
        cls, name: str, num_axes: int, data: ArrayLike | None
    ) -> None: ...

    @classmethod
    def check_numpy_array_features(
        cls,
        name: str,
        ref: NDArray[Any],
        data: None | ArrayLike,
        accuracy_critical: bool = False,  # noqa: FBT001
        report_failure: bool = True,  # noqa: FBT001
        report_success: bool = True,  # noqa: FBT001
    ) -> bool | None: ...

    @classmethod
    def check_numpy_array_allclose(
        cls,
        name: str,
        ref: NDArray[Any],
        data: ArrayLike,
        accuracy_critical: bool = False,  # noqa: FBT001
        rtol: float = 1e-05,
        atol: float = 1e-08,
        report_success: bool = True,  # noqa: FBT001
        report_failure: bool = True,  # noqa: FBT001
    ) -> bool: ...

    @classmethod
    def check_list(
        cls,
        name: str,
        ref: list[Any],
        data: list[Any] | None,
        entry_type: Any | None = None,
        accuracy_critical: bool = False,  # noqa: FBT001
        report_failure: bool = True,  # noqa: FBT001
        report_success: bool = True,  # noqa: FBT001
    ) -> bool: ...

    @classmethod
    def check_dict(
        cls,
        name: str,
        ref: dict[Any, Any],
        data: dict[Any, Any],
        *,
        target_keys: None | list[str] | set[str] = None,
        accuracy_critical: bool = False,
        report_failure: bool = True,
        report_success: bool = True,
    ) -> bool: ...

    @classmethod
    def check_tuple(
        cls,
        name: str,
        ref: tuple[Any],
        data: tuple[Any] | None,
        accuracy_critical: bool = False,  # noqa: FBT001
        report_failure: bool = True,  # noqa: FBT001
        report_success: bool = True,  # noqa: FBT001
    ) -> bool: ...

    @classmethod
    def check_scalar(
        cls,
        name: str,
        ref: complex | np.number[Any],
        data: complex | np.number[Any] | None,
        accuracy_critical: bool = False,  # noqa: FBT001
        rtol: float = 1e-5,
        atol: float = 1e-8,
        report_success: bool = True,  # noqa: FBT001
        report_failure: bool = True,  # noqa: FBT001
    ) -> bool: ...

    @classmethod
    def call_user(
        cls,
        f: Callable[..., T],
        *args: Any,
        stop_on_exception: bool = True,
        **kwargs: Any,
    ) -> Any: ...

    @classmethod
    def check_plot(
        cls,
        name: str,
        ref: Axes,
        plot: Axes,
        check_axes_scale: Literal[None, "x", "y", "xy"] = None,
        accuracy_critical: bool = False,  # noqa: FBT001
        report_failure: bool = True,  # noqa: FBT001
        report_success: bool = True,  # noqa: FBT001
    ) -> bool: ...

    @classmethod
    def check_dataframe(
        cls,
        name: str,
        ref: DataFrame,
        data: DataFrame,
        subset_columns: list[str] | None = None,
        check_values: bool = True,  # noqa: FBT001
        allow_order_variance: bool = True,  # noqa: FBT001
        display_input: bool = False,  # noqa: FBT001
        report_success: bool = True,  # noqa: FBT001
    ) -> bool: ...
