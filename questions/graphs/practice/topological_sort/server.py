import html
import random
from collections.abc import Callable, Iterable
from itertools import combinations
from typing import Any, TypeVar

import networkx as nx
import prairielearn as pl
from typing_extensions import assert_never

VertexT = TypeVar("VertexT")


def generate_pl_graph(
    g: nx.DiGraph | nx.Graph, label: str | None = None, rankdir: str = "LR"
) -> str:
    """
    Generates a string usable by a pl-graph element.
    @param graph nx.DiGraph
        graph to construct string representation of
    @return str
        representation of graph usable by a pl-graph element
    """
    visualize_graph = nx.nx_agraph.to_agraph(g)
    visualize_graph.graph_attr["rankdir"] = rankdir

    if label:
        for u, v in visualize_graph.edges():
            edge = visualize_graph.get_edge(u, v)
            edge.attr["label"] = edge.attr[label]

    return visualize_graph.to_string()


def grade_question_parameterized(
    data: pl.QuestionData,
    question_name: str,
    grade_function: Callable[[Any], tuple[bool | float, str | None]],
    weight: int = 1,
    feedback_field_name: str | None = None,
) -> None:
    """
    Grade question question_name, marked correct if grade_function(student_answer) returns True in
    its first argument. grade_function should take in a single parameter (which will be the submitted
    answer) and return a 2-tuple.
        - The first element of the 2-tuple should either be:
            - a boolean indicating whether the question should be marked correct
            - a partial score between 0 and 1, inclusive
        - The second element of the 2-tuple should either be:
            - a string containing feedback
            - None, if there is no feedback (usually this should only occur if the answer is correct)

    Note: if the feedback_field_name is the same as the question name,
    then the feedback_field_name does not need to be specified.
    """

    # Create the data dictionary at first
    data["partial_scores"][question_name] = {"score": 0.0, "weight": weight}

    try:
        submitted_answer = data["submitted_answers"][question_name]
    except KeyError:
        # Catch error if no answer submitted
        data["format_errors"][question_name] = "No answer was submitted"
        return

    # Try to grade, exiting if there's an exception
    try:
        result, feedback_content = grade_function(submitted_answer)

        # Check _must_ be done in this order. Int check is to deal with subclass issues
        if isinstance(result, bool):
            partial_score = 1.0 if result else 0.0
        elif isinstance(result, (float, int)):
            assert 0.0 <= result <= 1.0
            partial_score = result
        else:
            assert_never(result)

    except ValueError as err:
        # Exit if there's a format error
        data["format_errors"][question_name] = html.escape(str(err))
        return

    # Set question score if grading succeeded
    data["partial_scores"][question_name]["score"] = partial_score

    # Put all feedback here
    if feedback_content:
        # Check for unescaped bad stuff in feedback string
        if isinstance(submitted_answer, str):
            contains_bad_chars = all(x in submitted_answer for x in ("<", ">"))
            if contains_bad_chars and submitted_answer in feedback_content:
                raise ValueError(
                    f"Unescaped student input should not be present in the feedback for {question_name}."
                )

        data["partial_scores"][question_name]["feedback"] = feedback_content

        if not feedback_field_name:
            feedback_field_name = question_name

        data["feedback"][feedback_field_name] = feedback_content


def grade_toposort(
    data: pl.QuestionData,
    question_name: str,
    vertices: Iterable[VertexT],
    edges: Iterable[tuple[VertexT, VertexT]],
    transformation_function: Callable[[str], list[VertexT]],
) -> None:
    """
    Takes in data dictionary and checks if submission for topological ordering is correct.
    The submission is checked against the vertices and edges to check if it follows a valid topological ordering.
    transformation_function is used in order to handle multiple submission formats (comma separated list, just integers, etc).
    """

    def grader(submission: str) -> tuple[bool, str]:
        """
        The grader function takes in the submission and sets it as correct/incorrect, with feedback messages.
        """
        transformed_submission = transformation_function(submission)
        if not (
            set(transformed_submission) == set(vertices)
            and len(transformed_submission) == len(list(vertices))
        ):
            return (
                False,
                "Your input does not contain all vertices of the graph exactly once, or it contains vertices which are not in the graph.",
            )
        for i, j in edges:
            if transformed_submission.index(j) < transformed_submission.index(i):
                return False, f"The edge ({i},{j}) is not respected in your ordering."
        return True, "That's correct!"

    grade_question_parameterized(data, question_name, grader)


def generate(data: pl.QuestionData) -> None:
    num_vertices = 9
    num_edges = 12

    vertices = list(range(num_vertices))
    random.shuffle(vertices)

    possible_edges = [
        (vertices[i], vertices[j]) for (i, j) in combinations(range(num_vertices), 2)
    ]
    edges = random.sample(possible_edges, num_edges)

    graph: nx.DiGraph = nx.DiGraph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)

    data["params"]["graph"] = nx.readwrite.json_graph.node_link_data(
        graph, edges="links"
    )
    data["params"]["img"] = generate_pl_graph(graph)
    data["params"]["possible_answer"] = "".join(map(str, nx.topological_sort(graph)))


def grade(data: pl.QuestionData) -> None:
    graph: nx.DiGraph = nx.readwrite.json_graph.node_link_graph(
        data["params"]["graph"], edges="links"
    )
    grade_toposort(
        data,
        "r",
        graph.nodes,
        graph.edges(),
        lambda x: list(map(int, x.replace(" ", ""))),
    )
    pl.set_weighted_score_data(data)
