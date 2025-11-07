import random
from itertools import combinations, product
from typing import Any, Dict, List, Optional, Set, Tuple, cast

import networkx as nx

ClauseT = Tuple[int, int, int]
FormulaT = List[ClauseT]
ThreeSatAssignmentT = Set[int]
IndSetCertificateT = Set[Tuple[int, int]]


def is_literal_true(literal: int, assignment: ThreeSatAssignmentT):
    "Returns true if literal is true under the given assignment"
    return (literal in assignment) if literal > 0 else (-literal not in assignment)


def generate_three_sat_clause(num_vars: int) -> ClauseT:
    "Generate a random 3SAT clause with variables from [num_vars]"
    clause = tuple(random.sample(range(1, num_vars + 1), 3))
    return cast(ClauseT, tuple(random.choice([-1, 1]) * i for i in clause))


def is_clause_true(clause: ClauseT, assignment: ThreeSatAssignmentT) -> bool:
    "Returns true if clause is satisfied given the assignment in assignment"
    return any(is_literal_true(literal, assignment) for literal in clause)


def generate_true_clause(num_vars: int, assignment: ThreeSatAssignmentT) -> ClauseT:
    "Generates a true clause based on the assignment assignment"

    clause = generate_three_sat_clause(num_vars)

    # If clause is satisfied already, return
    if is_clause_true(clause, assignment):
        return clause

    # Otherwise, set a random literal to true
    new_clause = list(clause)
    index = random.choice(range(len(new_clause)))
    new_clause[index] = -new_clause[index]

    return cast(ClauseT, tuple(new_clause))


def generate_three_sat_formula(num_vars: int = 5, num_clauses: int = 6) -> FormulaT:
    "Generates a 3SAT formula with num_vars many variables and num_clauses many clauses"
    return [generate_three_sat_clause(num_vars) for _ in range(num_clauses)]


def generate_satisfied_formula(
    num_vars: int, num_clauses: int, assignment: ThreeSatAssignmentT
) -> FormulaT:
    "Generates a satisfied 3SAT formula with num_vars many variables and num_clauses many clauses based on the assignment in assignment"
    return [generate_true_clause(num_vars, assignment) for _ in range(num_clauses)]


def is_formula_satisfied(formula: FormulaT, assignment: ThreeSatAssignmentT) -> bool:
    "Returns true if the formula is satisfied under assignment"
    return all(is_clause_true(clause, assignment) for clause in formula)


def convert_3SAT_instance_to_ind_set_instance(three_sat_instance: FormulaT) -> nx.Graph:
    G = nx.Graph()

    for i, (i1, i2) in product(
        range(len(three_sat_instance)), combinations(range(3), 2)
    ):
        G.add_edge((i, i1), (i, i2))

    for (i1, clause1), (i2, clause2) in combinations(enumerate(three_sat_instance), 2):
        for (j1, literal1), (j2, literal2) in product(
            enumerate(clause1), enumerate(clause2)
        ):
            if literal1 == -literal2:
                G.add_edge((i1, j1), (i2, j2))

    return G


def is_ind_set_valid(graph: nx.Graph, k: int, certificate: Any) -> Tuple[bool, str]:
    "Returns true if certificate defines an independent set of size exactly k"

    if not isinstance(certificate, set):
        return (False, "Type of given independent set is not a set")

    for node in certificate:
        if node not in graph.nodes:
            return (
                False,
                f"Your independent set contains the element {node}, "
                "which is not a vertex of the graph",
            )

    size = len(certificate)
    if size != k:
        return (
            False,
            f"Your independent set has size {size}, "
            f"but is supposed to have size {k}.",
        )

    for u, v in graph.edges:
        if u in certificate and v in certificate:
            return (
                False,
                "Your independent set contains a pair of vertices, "
                f"namely {u} and {v}, which are adjacent in the graph.",
            )

    return (True, "")


def convert_3SAT_cert_to_ind_set_cert(
    three_sat_instance: FormulaT, assignment: ThreeSatAssignmentT
) -> IndSetCertificateT:
    "Convert a 3SAT certificate to an independent set certificate"
    ind_set_cert = set()

    for i, clause in enumerate(three_sat_instance):
        clause_to_iterate = list(enumerate(clause))
        random.shuffle(clause_to_iterate)

        for j, literal in clause_to_iterate:
            if is_literal_true(literal, assignment):
                ind_set_cert.add((i, j))
                break
        else:
            raise ValueError("No literals in clause are true")

    return ind_set_cert


def check_three_sat_formula_format(formula: Any) -> Tuple[bool, Optional[str]]:
    "Checks if formula is a correctly formatted 3SAT formula"
    if not isinstance(formula, list):
        return (False, "unsatisfiable_three_sat_instance should be a list.")

    for clause in formula:
        if (
            not isinstance(clause, tuple)
            or len(clause) != 3
            or not all(isinstance(variable, int) for variable in clause)
        ):
            return (
                False,
                (
                    "Each element in unsatisfiable_three_sat_instance "
                    "should be a tuple of integers of length 3."
                ),
            )

        if len(set(map(abs, clause))) != 3:
            return (False, "A variable may not show up in a clause more than once.")

    return (True, None)


def check_graph_format(graph: Any) -> Tuple[bool, Optional[str]]:
    "Checks if graph is a valid nx.Graph for this question"
    if not isinstance(graph, nx.Graph):
        return (False, "graph should be an instance of nx.Graph.")

    for node in graph.nodes:
        if (
            not isinstance(node, tuple)
            or len(node) != 2
            or not all(isinstance(elem, int) for elem in node)
        ):
            return (False, "Each node in the graph should be a 2-tuple of integers.")

    return (True, None)


def get_satisfying_assignment(formula: FormulaT) -> Optional[ThreeSatAssignmentT]:
    """
    From: https://jeffe.cs.illinois.edu/teaching/algorithms/notes/B-fastexpo.pdf#page=3
    """

    assignment_locations: Dict[int, int] = dict()
    assignment: Set[int] = set()

    def is_satisfiable_helper(formula_index: int) -> bool:
        if formula_index >= len(formula):
            return True

        for literal in formula[formula_index]:
            var_index = abs(literal)
            if var_index in assignment_locations and not is_literal_true(
                literal, assignment
            ):
                # If literal isn't true, keep searching for a true one
                continue

            if var_index not in assignment_locations:
                # Try setting literal to true
                assignment_locations[var_index] = formula_index
                if literal > 0:
                    assignment.add(var_index)

            if is_satisfiable_helper(formula_index + 1):
                return True

            if assignment_locations[var_index] == formula_index:
                # Otherwise, try again with literal must be set to false
                assignment_locations[var_index] = formula_index

                if var_index in assignment:
                    assignment.remove(var_index)
                else:
                    assignment.add(var_index)

            else:
                return False

        return False

    if is_satisfiable_helper(0):
        return assignment

    return None


def perform_flawed_reduction(formula: FormulaT) -> nx.Graph:
    "Performs a flawed 3SAT reduction"
    G = convert_3SAT_instance_to_ind_set_instance(formula)

    for i, (i1, i2) in product(range(len(formula)), combinations(range(3), 2)):
        G.remove_edge((i, i1), (i, i2))

    return G
