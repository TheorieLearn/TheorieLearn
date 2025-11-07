def grade(data):
    # Set partial credit
    data["partial_scores"] = {}
    if data["score"] != 1:
        data["score"] = 0

    answers = data["submitted_answers"]
    ques = data["params"]

    # Feedback Placeholders
    fb1 = ""
    fb2 = ""
    fb3 = ""
    fb4 = ""

    # Find the statement for each answer
    for q in ques["boil1"]:
        if answers["boil1"] == q["key"]:
            a1 = q["html"]
    for q in ques["boil2"]:
        if answers["boil2"] == q["key"]:
            a2 = q["html"]
    for q in ques["boil3"]:
        if answers["boil3"] == q["key"]:
            a3 = q["html"]
    for q in ques["boil4"]:
        if answers["boil4"] == q["key"]:
            a4 = q["html"]

    # Universal Declaration
    if answers["boil1"] != data["correct_answers"]["boil1"]["key"]:
        if a1 == "Pick an arbitrary string.":
            fb1 = "This is not an explicit declaration.  What is the string called?"
        elif a1 == "Let $w$ be a string of length $n$.":
            fb1 = "What is $n$?"
        elif a1 == "Let $|w|$ be an arbitrary non-negative integer.":
            fb1 = "But then what exactly is $w$?  What is the theorem about?"
        elif a1 == "Let $w^R$ be an arbitrary string.":
            fb1 = "But then what exactly is $w$?  What is the theorem about?"
        elif a1 == "Let $w$ be an arbitrary non-empty string.":
            fb1 = "Why does the string have to be non-empty?"

    # Conclusion
    if answers["boil2"] != data["correct_answers"]["boil2"]["key"]:
        if (
            a2 == "We conclude that $|x^R| = |x|$."
            or a2 == "We conclude that $|w^R| = |x|$."
        ):
            fb2 = "What is x?"
        elif a2 == "We conclude that $w^R = w$.":
            fb2 = "What are we trying to prove again?"

    # Induction Hypothesis
    if answers["boil3"] != data["correct_answers"]["boil3"]["key"]:
        if a3 == "Assume for any string $x$ where $|x| &gt; |w|$ that $|x^R| = |x|$.":
            fb3 = "An induction hypothesis needs to assume something about shorter strings, not longer strings."
        elif a3 == "Assume that the theorem is true for shorter strings.":
            fb3 = "Shorter than what?  What theorem?"
        elif a3 == "Assume true for all shorter strings.":
            fb3 = "Assume what?  Shorter than what?"
        elif a3 == "Assume all strings shorter than $w$ are true.":
            fb3 = "Strings can't be true"
        elif a3 == "Assume $|x| &lt; |w|$.":
            fb3 = "What is $x$? What does this have to do with induction?"
        elif a3 == "Assume $|w^R| = |w|$ for all shorter strings $w$.":
            fb3 = "$w$ is already fixed."
        elif a3 == "Assume $|w^R| = |w|.$":
            fb3 = "We can't just assume what we are trying to prove."
        elif a3 == "Assume $|x^R| = |x|.$":
            fb3 = "What is $x$? What does $x$ have to do with $w$?"
        elif (
            a3 == "Assume $|x^R| = |w|$ for all strings $x$ shorter than $w$."
            or a3 == "Assume $x^R = x$ for all strings $x$ shorter than $w$."
        ):
            fb3 = "Although syntactically correct, this is not semantically correct."

    # Cases
    if answers["boil4"] != data["correct_answers"]["boil4"]["key"]:
        if a4 == "There are two cases: $w= \\varepsilon$ or $w = xa$.":
            fb4 = "This is inconsistent with our recursive definition of strings."
        elif a4 == "There are two cases: $|w| = 0$ or not.":
            fb4 = "We always need to be specific."
        elif a4 == "There are three cases: $w = \\varepsilon$, $w = ax$, or $w = xa$.":
            fb4 = "This is inconsistent with our recursive definition of strings."

    data["feedback"]["boil1"] = fb1
    data["feedback"]["boil2"] = fb2
    data["feedback"]["boil3"] = fb3
    data["feedback"]["boil4"] = fb4
