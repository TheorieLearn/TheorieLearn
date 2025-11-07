from collections import deque
from typing import List

import networkx as nx

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def isSimple(s: str):
    return "(" not in s and ")" not in s and "/" not in s and "+" not in s

def is_balanced(s: str):
    stack = []
    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

def remove_outer_parentheses(s: str):
    if s is None:
        return None
    while s.startswith("(") and s.endswith(")") and is_balanced(s[1:-1]):
        s = s[1:-1]
    return s

def split_reg_expr(expr: str):
    parts = []
    current_part = []
    paren_depth = 0

    for char in expr:
        if char == '(':
            paren_depth += 1
            current_part.append(char)
        elif char == ')':
            paren_depth -= 1
            current_part.append(char)
        elif char == '+' and paren_depth == 0:
            parts.append(''.join(current_part).strip())
            current_part = []
        else:
            current_part.append(char)

    parts.append(''.join(current_part).strip())
    return parts

def processParenthesis(s: str):
    stack = []
    result: List[str] = []
    for i, char in enumerate(s):
        if char == '(':
            if not stack:
                start = i
            stack.append(char)
        elif char == ')':
            stack.pop()
            if not stack:
                result.append(s[start:i+1])
    if result:
        before_parentheses = s.split(result[0])[0]
        first_parentheses = result[0]
        after_parentheses = s[s.find(first_parentheses) + len(first_parentheses):]
        return before_parentheses, first_parentheses, after_parentheses
    else:
        return s


# ---------------------------------------------------------------------------
# Graph construction (NFA)
# ---------------------------------------------------------------------------

def genGraph(reg_expr: str, start_key, G):
    reg_expr = reg_expr.replace("|", "+")
    reg_expr = remove_outer_parentheses(reg_expr)

    G.add_node(start_key, label="q")
    temp_key = start_key

    if isSimple(reg_expr) and "*" not in reg_expr:
        temp_key += 1
        for s in reg_expr:
            if s == "e":
                s = "\u03B5"  # epsilon
            G.add_node(temp_key, label="")
            G.add_edge(temp_key - 1, temp_key, label=s)
            temp_key += 1
        G.add_node(temp_key - 1, label="f")
        return temp_key - 1

    parts = split_reg_expr(reg_expr)
    if len(parts) == 1:
        if "(" in reg_expr or ")" in reg_expr:
            paren_result = processParenthesis(reg_expr)
            if (type(paren_result) is tuple):
                before, paren, after = paren_result
        else:
            kleene_index = reg_expr.index('*')
            before = reg_expr[:kleene_index - 1]
            paren = reg_expr[kleene_index - 1]
            after = reg_expr[kleene_index:]

        if len(before) > 0:
            end_key = genGraph(before, start_key + 1, G)
            G.add_edge(start_key, start_key + 1, label="\u03B5")
            temp_key = end_key
            start_key = end_key

        end_key = genGraph(paren, temp_key + 1, G)
        G.add_edge(temp_key, temp_key + 1, label="\u03B5")

        if after.startswith("*"):
            G.add_edge(end_key, temp_key, label="\u03B5")
            temp_key = end_key + 1
            G.add_node(temp_key, label="f")
            G.add_edge(start_key, temp_key, label="\u03B5")
            G.add_edge(end_key, temp_key, label="\u03B5")
            after = after[1:]
            end_key = temp_key
        else:
            temp_key = end_key

        if len(after) > 0:
            end_key = genGraph(after, temp_key + 1, G)
            G.add_edge(temp_key, temp_key + 1, label="\u03B5")
        return end_key

    end_keys = []
    for part in parts:
        end_key = genGraph(part, temp_key + 1, G)
        G.add_edge(start_key, temp_key + 1, label="\u03B5")
        temp_key = end_key
        end_keys.append(end_key)

    temp_key = max(end_keys) + 1
    G.add_node(temp_key, label="f")
    for end_key in end_keys:
        G.add_edge(end_key, temp_key, label="\u03B5")
    return temp_key


def getEpsilonClosure(G, state):
    closure = {state}
    stack = [state]
    visited = {state: False for state in G.nodes}
    while stack:
        curr = stack.pop()
        visited[curr] = True
        for neighbor in G.neighbors(curr):
            if not visited[neighbor]:
                edge = G.edges[curr, neighbor]["label"]
                if edge == "\u03B5":
                    closure.add(neighbor)
                    stack.append(neighbor)
    return closure


# ---------------------------------------------------------------------------
# Function: Generate strings accepted by regex
# ---------------------------------------------------------------------------

def genStrings(reg):
    """
    Generates a list of up to 20 strings from the language of the given regex.
    """
    if reg.strip() == "":
        return sorted({""})

    reg = reg.replace(" ", "")
    reg = reg.replace("+*", "+e*")
    reg = reg.replace("e*", "e")

    G = nx.DiGraph()
    endKey = genGraph(reg, 0, G)
    EpsilonDict = {state: getEpsilonClosure(G, state) for state in G.nodes}

    string_list = set()
    queue = deque([(0, "")])  # true BFS queue

    while queue and len(string_list) < 20:
        curr, built = queue.popleft()

        # if this is an accepting state, record the string
        if curr == endKey or endKey in EpsilonDict[curr]:
            string_list.add(built)

        # explore neighbors
        for neighbor in G.neighbors(curr):
            edge = G.edges[curr, neighbor].get("label", None)
            if edge != "\u03B5" and type(edge)==str:
                queue.append((neighbor, built + edge))
            else:
                queue.append((neighbor, built))

    string_list = {s if s != "" else "\u03B5" for s in string_list}

    result = sorted(string_list, key=lambda x: (len(x), x))
    if "\u03B5" in result:
        result.insert(0, result.pop(result.index("\u03B5")))
    return result



# ---------------------------------------------------------------------------
# PrairieLearn grade() entry point
# ---------------------------------------------------------------------------

def grade(data):
    regex = data["submitted_answers"]["regex"]

    try:
        if not is_balanced(regex):
            raise ValueError("Unbalanced parentheses in regex.")
        strings = genStrings(regex)
        formatted = "<br>".join(f"`{s}`" for s in strings)
        data["score"] = 1
        data["feedback"] = {
            "message": f"Accepted strings for {regex}:<br>{formatted}"
        }
    except Exception as e:
        data["score"] = 0
        data["feedback"] = {
            "message": f"Error generating strings: {str(e)}"
        }
