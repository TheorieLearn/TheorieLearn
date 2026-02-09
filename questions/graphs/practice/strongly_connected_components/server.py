import html
import re
from collections.abc import Callable, Iterable
from typing import Any, TypeVar

import networkx as nx
import prairielearn as pl
from networkx import Graph
from text_unidecode import unidecode
from typing_extensions import assert_never

VertexT = TypeVar("VertexT")


def sanitize_input(student_ans: str) -> str:
    "Run unidecode and remove any extra spaces"

    return unidecode(student_ans).replace(" ", "")


def tokenize_string(string: str) -> list[str]:
    "Removes all spaces from string and splits on comma outside parenthesis into a list"
    # Regex from here: https://stackoverflow.com/questions/26633452/how-to-split-by-commas-that-are-not-within-parentheses
    string = sanitize_input(string)
    return list(re.split(r",\s*(?![^()]*\))", string.replace(" ", "").strip(",")))


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


def tokenize_string_set(string: str) -> list[str]:
    "Turn string representing a set as input into a list of tokens."
    string = string.strip()
    # Handle empty set symbol
    if string == "∅":
        string = "{}"
    elif not string.startswith("{") or not string.endswith("}"):
        raise ValueError(
            "Make sure to format your answer with curly braces to denote a set"
        )
    string = string[1:-1]
    return tokenize_string(string)


def grade_question_tokenized(
    data: pl.QuestionData,
    question_name: str,
    expected_answer_optional: str | None = None,
    weight: int = 1,
) -> None:
    "Grade question named question_name where student input needs to be tokenized with a set"

    expected_answer = expected_answer_optional or data["correct_answers"][question_name]
    is_expected_set = (
        expected_answer.startswith("{") and expected_answer.endswith("}")
    ) or expected_answer == "∅"
    tokenize_function = (
        tokenize_string_set if is_expected_set else tokenize_string_without_set
    )
    grade_question_parameterized(
        data,
        question_name,
        lambda student_ans: (
            set(tokenize_function(student_ans))
            == set(tokenize_function(expected_answer)),
            None,
        ),
        weight,
    )


def tokenize_string_without_set(student_answer: str) -> list[str]:
    "Wrapper Function of tokenize_string that Checks if Student has Erroneous Set Braces"
    if student_answer.startswith("{") or student_answer.endswith("}"):
        raise ValueError(
            "This input field is not a set, so it does not require curly braces"
        )
    return tokenize_string(student_answer)


def generate(data: pl.QuestionData) -> None:
    num_sscs = 0
    isolated = 1
    n = 10
    m = 12
    while num_sscs < 4 or num_sscs > 6 or isolated != 0:
        g = nx.gnm_random_graph(n, m, seed=None, directed=True)
        meta_graph = nx.condensation(g)
        isolated = len(list(nx.isolates(g)))
        num_sscs = meta_graph.number_of_nodes()

    # Spread out edges so they're easier to see
    mapping: dict[int, str] = {
        n: "".join(map(str, sorted(meta_graph.nodes[n]["members"]))) for n in meta_graph
    }
    meta_graph_relabeled: Graph = nx.relabel_nodes(meta_graph, mapping, copy=False)

    data["correct_answers"]["meta_v"] = ", ".join(map(str, meta_graph_relabeled.nodes))
    data["correct_answers"]["meta_e"] = ", ".join(
        f"{u}->{v}" for u, v in meta_graph_relabeled.edges
    )
    data["correct_answers"]["meta_topo"] = ", ".join(
        map(str, nx.topological_sort(nx.DiGraph(meta_graph_relabeled)))
    )

    data["params"]["img"] = generate_pl_graph(g)
    data["params"]["meta_v"] = list(meta_graph_relabeled.nodes)
    data["params"]["meta_e"] = list(meta_graph_relabeled.edges)


def parse(data: pl.QuestionData) -> None:
    # First, process the submitted vertices
    meta_v = data["submitted_answers"]["meta_v"]
    if meta_v:
        data["submitted_answers"]["meta_v"] = ", ".join(
            "".join(sorted(i)) for i in (tokenize_string(meta_v))
        )

    # Next, process the submitted toposort
    meta_topo = data["submitted_answers"]["meta_topo"]
    if meta_topo:
        data["submitted_answers"]["meta_topo"] = ", ".join(
            "".join(sorted(i)) for i in (tokenize_string(meta_topo))
        )

    # Finally, process the submitted edges
    meta_e = data["submitted_answers"]["meta_e"]
    if meta_e:
        edge_list = meta_e.replace(" ", "").split(",")
        new_edge_arr = []
        for edge in edge_list:
            new_edge = ["".join(sorted(v)) for v in edge.split("->")]
            new_edge_arr.append("->".join(new_edge))
        data["submitted_answers"]["meta_e"] = ", ".join(new_edge_arr)


def grade(data: pl.QuestionData) -> None:
    grade_question_tokenized(data, "meta_v")
    grade_question_tokenized(data, "meta_e")

    vertices = data["params"]["meta_v"]
    edges = data["params"]["meta_e"]

    grade_toposort(data, "meta_topo", vertices, edges, tokenize_string)

    pl.set_weighted_score_data(data)
