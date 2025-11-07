import re

from automata.fa.dfa import DFA
from theorielearn.automata_utils.fa_utils import get_minimum_counterexample
from theorielearn.regular_expressions.parser import compute_nfa_from_regex_lines


# function: infer the user's alphabet based on what they enter, defaulting to 01
def infer_alphabet(*regexes):
    """Infer alphabet from regex symbols (letters or digits)."""
    symbols = set()
    for r in regexes:
        #Collect alphanumeric symbols used in the regex
        symbols |= set(re.findall(r"[A-Za-z0-9]", r))
    #Default to binary alphabet if nothing found
    return symbols or set("01")


def grade(data):
    answers = data["submitted_answers"]
    regex1 = answers["regex1"].strip()
    regex2 = answers["regex2"].strip()

    alphabet = infer_alphabet(regex1, regex2)

    try:
        # Step 1: Convert regex → DFA
        dfa1 = DFA.from_nfa(
            compute_nfa_from_regex_lines(regex1, alphabet), retain_names=False
        ).minify()
        dfa2 = DFA.from_nfa(
            compute_nfa_from_regex_lines(regex2, alphabet), retain_names=False
        ).minify()

        #compare DFAs
        equal = dfa1 == dfa2
        subset = dfa1.issubset(dfa2)
        superset = dfa1.issuperset(dfa2)

        # find a counter example for the user
        counterexample = get_minimum_counterexample(dfa1, dfa2)[0]


        #building feedback message
        if equal:
            msg = f"Equivalent!\n{regex1} and {regex2} describe the same language."
            data["score"] = 1.0
        else:
            lines = []
            if subset:
                lines.append(f"{regex1} is a subset of {regex2}.")
            elif superset:
                lines.append(f"{regex2} is a subset of {regex1}.")
            else:
                lines.append(f"{regex1} and {regex2} are not equivalent!")

            if counterexample:
                #Determine which regex accepts/rejects the counterexample
                accepts1 = dfa1.accepts_input(counterexample)
                accepts2 = dfa2.accepts_input(counterexample)
                if accepts1 and not accepts2:
                    lines.append(
                        f"Counterexample: '{counterexample}' is accepted by Regex 1 but rejected by Regex 2."
                    )
                elif accepts2 and not accepts1:
                    lines.append(
                        f"Counterexample: '{counterexample}' is accepted by Regex 2 but rejected by Regex 1."
                    )
                else:
                    lines.append(f"Counterexample string: {counterexample}")

            msg = "\n".join(lines)
            data["score"] = 0.0  # red grade for mismatch

        data["feedback"] = {"message": msg}

    except Exception as e:
        data["feedback"] = {"message": f"Error: {type(e).__name__}: {e}"}
        data["score"] = 0.0
