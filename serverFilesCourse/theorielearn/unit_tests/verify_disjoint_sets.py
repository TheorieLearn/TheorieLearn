import pytest
from theorielearn.disjoint_sets.server_base import DisjointSetUnion


@pytest.mark.parametrize(
    "unions, path_compression, expected_result",
    [
        (
            [(5, 2), (6, 3), (8, 6), (5, 3), (0, 5), (8, 3), (2, 0)],
            False,
            [6, -1, 5, 6, -1, 6, -6, -1, 6, -1],
        ),
        (
            [(1, 7), (3, 4), (7, 3), (7, 4), (2, 5)],
            True,
            [-1, -4, -2, 1, 3, 2, -1, 1, -1, -1],
        ),
    ],
)
def test_disjoint_set_union(
    unions: list[tuple[int, int]], path_compression: bool, expected_result: list[int]
) -> None:
    dsu = DisjointSetUnion(10, path_compression)
    for a, b in unions:
        dsu.union(a, b)
    assert dsu.get_parent() == expected_result
