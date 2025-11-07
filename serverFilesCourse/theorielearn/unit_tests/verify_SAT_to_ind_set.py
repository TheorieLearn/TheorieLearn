from typing import Any, List, Tuple

import networkx as nx
import pytest
import theorielearn.reductions.SAT_to_ind_set as sti

ASSIGNMENT = {2, 6, 8, 10}

TRUE_CLAUSE_1 = (2, -6, -8)
TRUE_CLAUSE_2 = (6, 2, 4)
TRUE_CLAUSE_3 = (-6, -2, -3)
TRUE_CLAUSE_4 = (3, 4, -5)

SATISFIABLE_FORMULA = [TRUE_CLAUSE_1, TRUE_CLAUSE_2, TRUE_CLAUSE_3, TRUE_CLAUSE_4]

FALSE_CLAUSE_1 = (-2, -6, -8)
FALSE_CLAUSE_2 = (-2, 4, -8)
FALSE_CLAUSE_3 = (-2, 4, 5)


@pytest.mark.parametrize(
    "literal, expected", [(-4, True), (2, True), (-2, False), (4, False)]
)
def verify_is_literal_true(literal: int, expected: bool) -> None:
    assert sti.is_literal_true(literal, ASSIGNMENT) is expected


def check_clause_correct_format(clause: sti.ClauseT, num_vars: int) -> None:
    assert isinstance(clause, tuple)
    assert len({abs(x) for x in clause}) == 3
    assert all(0 < abs(x) <= num_vars for x in clause)


@pytest.mark.parametrize("num_vars", [4, 5, 10, 20, 50, 100])
def verify_generate_three_sat_clause(num_vars: int) -> None:
    iterations = 20
    for _ in range(iterations):
        clause = sti.generate_three_sat_clause(num_vars)
        check_clause_correct_format(clause, num_vars)


@pytest.mark.parametrize(
    "clause, expected",
    [
        (TRUE_CLAUSE_1, True),
        (TRUE_CLAUSE_2, True),
        (TRUE_CLAUSE_3, True),
        (TRUE_CLAUSE_4, True),
        (FALSE_CLAUSE_1, False),
        (FALSE_CLAUSE_2, False),
        (FALSE_CLAUSE_3, False),
    ],
)
def verify_is_clause_true(clause: sti.ClauseT, expected: bool) -> None:
    assert sti.is_clause_true(clause, ASSIGNMENT) is expected


def verify_generate_true_clause() -> None:
    iterations = 20
    num_vars = max(ASSIGNMENT)

    for _ in range(iterations):
        assert sti.is_clause_true(
            sti.generate_true_clause(num_vars, ASSIGNMENT), ASSIGNMENT
        )


# ------------------- Independent set certificate helpers ----------------------

EdgeListT = List[Tuple[Tuple[int, int], Tuple[int, int]]]


def edges_to_graph(edges: List[Tuple[Any, Any]]) -> nx.Graph:
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


FORMULA_1 = [(1, -3, 2), (3, 2, -1)]
FORMULA_2 = [(1, 3, 2), (2, -3, -1)]

EDGE_LIST_1 = [
    ((0, 0), (1, 2)),
    ((0, 0), (0, 2)),
    ((0, 0), (0, 1)),
    ((0, 1), (1, 0)),
    ((0, 1), (0, 2)),
    ((1, 0), (1, 1)),
    ((1, 0), (1, 2)),
    ((1, 1), (1, 2)),
]

FLAWED_EDGE_LIST_1 = [((0, 0), (1, 2)), ((0, 1), (1, 0))]

EDGE_LIST_2 = [
    ((0, 0), (1, 2)),
    ((0, 0), (0, 2)),
    ((0, 0), (0, 1)),
    ((0, 1), (1, 1)),
    ((0, 1), (0, 2)),
    ((1, 0), (1, 1)),
    ((1, 0), (1, 2)),
    ((1, 1), (1, 2)),
]

FLAWED_EDGE_LIST_2 = [((0, 0), (1, 2)), ((0, 1), (1, 1))]

EDGE_LIST_1_2_IND_SET_1 = {(1, 1)}
EDGE_LIST_1_2_IND_SET_2 = {(0, 0), (1, 1)}
EDGE_LIST_1_IND_SET_3 = {(0, 2), (1, 0)}
EDGE_LIST_2_IND_SET_3 = {(0, 2), (1, 2)}

EDGE_LIST_1_NON_IND_SET_1 = {(0, 0), (1, 2)}
EDGE_LIST_2_NON_IND_SET_1 = {(0, 1), (1, 1)}

# ------------------ Start tests for certificate functions ---------------------


@pytest.mark.parametrize(
    "formula, assignment, expected",
    [
        ([TRUE_CLAUSE_1], ASSIGNMENT, True),
        ([TRUE_CLAUSE_1, TRUE_CLAUSE_3], ASSIGNMENT, True),
        (
            [TRUE_CLAUSE_1, TRUE_CLAUSE_2, TRUE_CLAUSE_3, TRUE_CLAUSE_4],
            ASSIGNMENT,
            True,
        ),
        ([FALSE_CLAUSE_1, FALSE_CLAUSE_2], ASSIGNMENT, False),
        ([TRUE_CLAUSE_1, TRUE_CLAUSE_2, FALSE_CLAUSE_3], ASSIGNMENT, False),
        (
            [TRUE_CLAUSE_1, FALSE_CLAUSE_1, TRUE_CLAUSE_2, FALSE_CLAUSE_2],
            ASSIGNMENT,
            False,
        ),
    ],
)
def verify_is_formula_satisfied(
    formula: sti.FormulaT, assignment: sti.ThreeSatAssignmentT, expected: bool
) -> None:
    assert sti.is_formula_satisfied(formula, assignment) is expected


@pytest.mark.parametrize(
    "formula, edges", [(FORMULA_1, EDGE_LIST_1), (FORMULA_2, EDGE_LIST_2)]
)
def verify_convert_3SAT_instance_to_ind_set_instance(
    formula: sti.FormulaT, edges: EdgeListT
) -> None:
    result_graph = sti.convert_3SAT_instance_to_ind_set_instance(formula)
    reference_graph = edges_to_graph(edges)

    assert result_graph.nodes == reference_graph.nodes
    assert result_graph.edges == reference_graph.edges


@pytest.mark.parametrize(
    "edges, k, certificate, expected",
    [
        (EDGE_LIST_1, 1, EDGE_LIST_1_2_IND_SET_1, True),
        (EDGE_LIST_1, 2, EDGE_LIST_1_2_IND_SET_2, True),
        (EDGE_LIST_1, 2, EDGE_LIST_1_IND_SET_3, True),
        (EDGE_LIST_1, 1, EDGE_LIST_1_2_IND_SET_2, False),
        (EDGE_LIST_1, 2, EDGE_LIST_1_NON_IND_SET_1, False),
        (EDGE_LIST_1, 3, {(0, 0), (0, 2), (1, 1)}, False),
        (EDGE_LIST_2, 1, EDGE_LIST_1_2_IND_SET_1, True),
        (EDGE_LIST_2, 2, EDGE_LIST_1_2_IND_SET_2, True),
        (EDGE_LIST_2, 2, EDGE_LIST_2_IND_SET_3, True),
        (EDGE_LIST_2, 1, EDGE_LIST_1_2_IND_SET_2, False),
        (EDGE_LIST_2, 2, EDGE_LIST_2_NON_IND_SET_1, False),
        (EDGE_LIST_2, 3, {(0, 0), (0, 2), (1, 1)}, False),
    ],
)
def verify_is_ind_set_valid(
    edges: EdgeListT, k: int, certificate: sti.IndSetCertificateT, expected: bool
) -> None:
    assert sti.is_ind_set_valid(edges_to_graph(edges), k, certificate)[0] is expected


@pytest.mark.parametrize(
    "formula, assignment",
    [
        (FORMULA_1, {2}),
        (FORMULA_1, {}),
        (FORMULA_2, {2}),
        (FORMULA_2, {1}),
        ([TRUE_CLAUSE_1, TRUE_CLAUSE_3], ASSIGNMENT),
        ([TRUE_CLAUSE_1, TRUE_CLAUSE_2, TRUE_CLAUSE_3, TRUE_CLAUSE_4], ASSIGNMENT),
    ],
)
def verify_convert_3SAT_cert_to_ind_set_cert(
    formula: sti.FormulaT, assignment: sti.ThreeSatAssignmentT
) -> None:
    is_satisfied = sti.is_formula_satisfied(formula, assignment)
    converted_graph = sti.convert_3SAT_instance_to_ind_set_instance(formula)
    ind_set = sti.convert_3SAT_cert_to_ind_set_cert(formula, assignment)

    assert (
        sti.is_ind_set_valid(converted_graph, len(ind_set), ind_set)[0] is is_satisfied
    )


def verify_convert_3SAT_cert_to_ind_set_cert_exception() -> None:
    formula = [FALSE_CLAUSE_1, FALSE_CLAUSE_2, FALSE_CLAUSE_3]
    with pytest.raises(ValueError):
        sti.convert_3SAT_cert_to_ind_set_cert(formula, ASSIGNMENT)


@pytest.mark.parametrize(
    "formula, expected",
    [
        ("stuff", False),
        (4, False),
        ([("stuff", 4, 5)], False),
        ([TRUE_CLAUSE_1, (1, 2, 3, 4)], False),
        ([FALSE_CLAUSE_1, (-3, 3, 4)], False),
        ([TRUE_CLAUSE_1], True),
        ([FALSE_CLAUSE_1], True),
        ([TRUE_CLAUSE_1, FALSE_CLAUSE_2, TRUE_CLAUSE_2], True),
    ],
)
def verify_check_three_sat_formula_format(formula, expected: bool) -> None:
    assert sti.check_three_sat_formula_format(formula)[0] is expected


class VerifyCheckGraphFormat:
    @pytest.mark.parametrize("argument", ["stuff", 4, (4, 3)])
    def verify_check_graph_format_false(self, argument) -> None:
        assert sti.check_graph_format(argument)[0] is False

    @pytest.mark.parametrize(
        "edges, expected",
        [
            ([(1, 2), (2, 3), (3, 4)], False),
            ([((1, 2, 3), (3, 4, 5)), ((1, 2, 4), (2, 4, 5))], False),
            ([((4, 3), (1, 2)), (("d", "a"), ("b", "a"))], False),
            (EDGE_LIST_1, True),
            (EDGE_LIST_2, True),
        ],
    )
    def verify_check_graph_format(self, edges: EdgeListT, expected: bool) -> None:
        assert sti.check_graph_format(edges_to_graph(edges))[0] is expected


@pytest.mark.parametrize(
    "argument, size",
    [
        ("stuff", 5),
        (4, 1),
        ({(4, (1, 2))}, 1),
        (((1, 1), (0, 0)), 1),
        (EDGE_LIST_1_2_IND_SET_2, 3),
    ],
)
def verify_is_ind_set_valid_false(argument: Any, size: int) -> None:
    graph = edges_to_graph(EDGE_LIST_1)
    assert sti.is_ind_set_valid(argument, size, graph)[0] is False


UNSAT_FORMULA = [
    (1, 2, 3),
    (1, 2, -3),
    (1, -2, 3),
    (1, -2, -3),
    (-1, 2, 3),
    (-1, 2, -3),
    (-1, -2, 3),
    (-1, -2, -3),
]


@pytest.mark.parametrize(
    "formula, expected",
    [(SATISFIABLE_FORMULA, True), (UNSAT_FORMULA, False), (UNSAT_FORMULA[:-1], True)],
)
def verify_get_satisfying_assignment(formula: sti.FormulaT, expected: bool) -> None:
    if expected:
        assignment = sti.get_satisfying_assignment(formula)
        assert assignment is not None
        assert sti.is_formula_satisfied(formula, assignment)
    else:
        assert sti.get_satisfying_assignment(formula) is None


@pytest.mark.parametrize(
    "num_vars, num_clauses", [(4, 10), (10, 20), (100, 200), (40, 50)]
)
def verify_generate_three_sat_formula(num_vars: int, num_clauses: int) -> None:
    iterations = 20
    for _ in range(iterations):
        formula = sti.generate_three_sat_formula(num_vars, num_clauses)
        assert len(formula) == num_clauses
        assert sti.check_three_sat_formula_format(formula)[0]

        for clause in formula:
            check_clause_correct_format(clause, num_vars)


def verify_generate_satisfied_formula() -> None:
    iterations = 50
    num_vars = 10
    for num_clauses in range(iterations):
        formula = sti.generate_satisfied_formula(num_vars, num_clauses, ASSIGNMENT)
        assert len(formula) == num_clauses
        assert sti.check_three_sat_formula_format(formula)[0]
        assert sti.is_formula_satisfied(formula, ASSIGNMENT)

        for clause in formula:
            check_clause_correct_format(clause, num_vars)


@pytest.mark.parametrize(
    "formula, edges", [(FORMULA_1, FLAWED_EDGE_LIST_1), (FORMULA_2, FLAWED_EDGE_LIST_2)]
)
def verify_perform_flawed_reduction(formula: sti.FormulaT, edges: EdgeListT) -> None:
    result_graph = sti.perform_flawed_reduction(formula)
    reference_graph = edges_to_graph(edges)

    assert result_graph.edges == reference_graph.edges
