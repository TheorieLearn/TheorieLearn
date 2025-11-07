from theorielearn.regular_expressions.parser import compute_nfa_from_regex_lines


def grade(data):
    regex = data["submitted_answers"]["regex"]
    test_string = data["submitted_answers"]["test_string"]

    try:
        nfa = compute_nfa_from_regex_lines(regex)
        accepted = nfa.accepts_input(test_string)

        if accepted:
            data["score"] = 1
            data["feedback"] = {
                "message": f"The string {test_string} is accepted by the regex {regex}."
            }
        else:
            data["score"] = 0
            data["feedback"] = {
                "message": f"The string {test_string} is not accepted by the regex {regex}."
            }

    except Exception as e:
        data["score"] = 0
        data["feedback"] = {"message": f"Error: {str(e)}"}
