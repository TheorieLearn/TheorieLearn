import random
from typing import Dict

import networkx as nx
import theorielearn.shared_utils as su


def inorder(tree: Dict[str, str], node: str) -> str:
    "Returns an inorder traversal of a tree as a string"
    if node not in tree.keys():
        return node
    children = tree[node]
    return inorder(tree, children[0]) + node + inorder(tree, children[1])


def preorder(tree: Dict[str, str], node: str) -> str:
    "Returns a preorder traversal of a tree"
    if node not in tree.keys():
        return node
    children = tree[node]
    return node + preorder(tree, children[0]) + preorder(tree, children[1])


def postorder(tree: Dict[str, str], node: str) -> str:
    "Returns an postorder traversal of a tree"
    if node not in tree.keys():
        return node
    children = tree[node]
    return postorder(tree, children[0]) + postorder(tree, children[1]) + node


def generate(data: su.QuestionData) -> None:
    instructors = ["Dakshita", "Jeff"]
    tas = [
        "Christian",
        "Eliot",
        "Shubhang",
        "Cosmo",
        "James",
        "Stav",
        "David",
        "Robert",
        "Tanvi",
    ]
    num_nodes = 21
    rand_tree = nx.full_rary_tree(2, num_nodes)

    alphabet = list("BCDFGHJKLMNPQRSTVWXYZ")
    random.shuffle(alphabet)
    alphabet_list = "".join(alphabet)

    int_to_letter = {i: alphabet_list[i] for i in range(num_nodes)}
    nx.relabel_nodes(rand_tree, int_to_letter, copy=False)
    root = int_to_letter[0]
    tree_dict = nx.dfs_successors(rand_tree, root)
    pre_order = preorder(tree_dict, root)
    in_order = inorder(tree_dict, root)
    post_order = postorder(tree_dict, root)
    left_of_root = tree_dict[root][0]
    right_of_root = tree_dict[root][1]

    correct_answers = data["correct_answers"]
    params = data["params"]

    params["who"] = random.choice(instructors + tas)
    qtype = random.randint(1, 3)

    correct_answers["root"] = root
    if qtype == 1:
        correct_answers["ans"] = in_order
        correct_answers["first-left"] = preorder(tree_dict, left_of_root)
        correct_answers["first-right"] = preorder(tree_dict, right_of_root)
        correct_answers["second-left"] = postorder(tree_dict, left_of_root)
        correct_answers["second-right"] = postorder(tree_dict, right_of_root)
        params["first"] = "preorder"
        params["firstl"] = "substring"
        params["firstr"] = "suffix"
        params["second"] = "postorder"
        params["secondl"] = "prefix"
        params["secondr"] = "substring"
        params["answer"] = "inorder"
        params["inorder"] = None
        params["preorder"] = pre_order
        params["postorder"] = post_order

    elif qtype == 2:
        correct_answers["ans"] = pre_order
        correct_answers["first-left"] = inorder(tree_dict, left_of_root)
        correct_answers["first-right"] = inorder(tree_dict, right_of_root)
        correct_answers["second-left"] = postorder(tree_dict, left_of_root)
        correct_answers["second-right"] = postorder(tree_dict, right_of_root)
        params["first"] = "inorder"
        params["firstl"] = "prefix"
        params["firstr"] = "suffix"
        params["second"] = "postorder"
        params["secondl"] = "prefix"
        params["secondr"] = "substring"
        params["answer"] = "preorder"
        params["inorder"] = in_order
        params["preorder"] = None
        params["postorder"] = post_order

    elif qtype == 3:
        correct_answers["ans"] = post_order
        correct_answers["first-left"] = inorder(tree_dict, left_of_root)
        correct_answers["first-right"] = inorder(tree_dict, right_of_root)
        correct_answers["second-left"] = preorder(tree_dict, left_of_root)
        correct_answers["second-right"] = preorder(tree_dict, right_of_root)
        params["first"] = "inorder"
        params["firstl"] = "prefix"
        params["firstr"] = "suffix"
        params["second"] = "preorder"
        params["secondl"] = "substring"
        params["secondr"] = "suffix"
        params["answer"] = "postorder"
        params["inorder"] = in_order
        params["preorder"] = pre_order
        params["postorder"] = None

    else:
        raise Exception(f"Invalid qtype {qtype}")
