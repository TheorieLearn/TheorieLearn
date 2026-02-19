from code_feedback import Feedback
from language_definition import generateLanguage
from nltk.grammar import CFG, Nonterminal, Production
from pl_helpers import name, points
from pl_unit_test import PLTestCase


def splitProdRhs(prod):
    """
    Converts production rules from
        S -> '00' S '1'
    into
        S -> '0' '0' S '1'
    """
    new_rhs = []
    for symbol in prod.rhs():
        if isinstance(symbol, str):
            new_rhs += list(symbol)
        else:
            new_rhs.append(symbol)

    return Production(prod.lhs(), new_rhs)


def exploreCFG(cfg, length_limit):
    """
    Generate strings with the CFG,
    without ever allowing an intermediate expression to exceed the length_limit.

    Note that not all strings with length <= length_limit that can be generated will be generated.
    For example, with S -> 1S | e and length_limit = 2, we won't be able to generate "11"
    because in the sequence S -> 1S -> 11S -> 11, 11S is too long and we would stop exploring there.
    """
    cfg = CFG(cfg.start(), [splitProdRhs(prod) for prod in cfg.productions()])

    finished = set()  # Expressions with no nonterminals left
    visited = set()  # Expressions with nonterminals that have already been explored
    to_explore = [(cfg.start(),)]

    while to_explore:
        expr = to_explore.pop()
        if expr in visited or len(expr) > length_limit:
            continue

        for i in range(len(expr)):
            if isinstance(expr[i], Nonterminal):
                break
        else:
            finished.add(expr)
            continue
        visited.add(expr)

        for prod in cfg.productions(lhs=expr[i]):
            to_explore.append(expr[:i] + prod.rhs() + expr[i + 1 :])

    return finished


MAX_LENGTH_TO_CHECK = 14


class Test(PLTestCase):
    student_code_file = 'submission.txt'
    @points(1)
    @name("Check that CFG is correct")
    def test_0(self):
        studentL = {
            "".join(s) for s in exploreCFG(self.st.cfg, MAX_LENGTH_TO_CHECK + 3)
        }
        # The "+ 3" is for wiggle room
        # See exploreCFG documentation for an explanation of why this is necessary

        studentL = {s for s in studentL if len(s) <= MAX_LENGTH_TO_CHECK}
        correctL = generateLanguage(MAX_LENGTH_TO_CHECK)

        falsePositives = studentL.difference(correctL)
        if falsePositives:
            Feedback.add_feedback(
                "Your CFG generated the string "
                f"'{min(falsePositives, key=lambda s: len(s))}', "
                "which is not in the language."
            )
            return

        falseNegatives = correctL.difference(studentL)
        if falseNegatives:
            Feedback.add_feedback(
                "Your CFG did not generate the string "
                f"'{min(falseNegatives, key=lambda s: len(s))}', "
                "which is in the language."
            )
            return

        Feedback.set_score(1)
