import random

import chevron
import prairielearn as pl
import sympy
from theorielearn.shared_utils import QuestionData

from theorielearn.recurrence_equations.utils import gen_for, gen_line


# Note - if more than one option for the type of for loop is "True", one will be chosen at random from the options
def generate_recurrence(
    data: QuestionData,
    *,
    lines_of_code: int,  # Total Code, including lines inside of for loops, but not the for loops themselves
    lines_inside_for_loops: int,  # The lines inside of for loops
    for_loop_count: int,  # How many nested for loops
    log_loop=False,  # The for loop will have log(n) iterations.
    factor_n_for_loops=False,  # The for loop will have c*n iterations. Possible i += c instead of 1.
    const_for_loops=False,  # The for loop will have c iterations
    n_for_loops=False,  # The for loop will have exactly n iterations
    no_recursion=False,  # Zero recursive calls will be made. If False, at least one recursive call is guaranteed.
) -> None:
    n = sympy.symbols("n")
    T = sympy.Function("T")
    O = sympy.Function("O")

    non_standard_log = False  # A log loop like i < n**2 or i *= 4 will be created.
    # Capability for this is in the code but I'm not 100% Confident the answers are correct. The
    # reason is because the coefficients of T(n) are expected to be exact for the other scenarios, but this doesn't identify
    # exact differences like log base 2 ~ log base 3 or log(n^2) = 2logn ~ log n.
    # I'm still leaving it in here just not as a parameter so it's usable with warning

    forOpts = {
        "n_for_loops": n_for_loops,
        "factor_n_for_loops": factor_n_for_loops,
        "log_loop": log_loop,
        "const_for_loops": const_for_loops,
        "non_standard_log": non_standard_log,
    }

    ExternalFunctions = [
        "Mystery",
        "Magic",
        "ChatGPT",
        "Math",
        "Read",
        "Compute",
        "Navigate",
        "Invert",
        "Travel",
        "Access",
        "Jump",
        "Teleport",
        "SelfDestruct",
        "Contemplate",
        "Cache",
        "Request",
    ]

    # The main function
    funcname = random.choice(ExternalFunctions)
    ExternalFunctions.remove(funcname)
    # The one we're wondering how many times it gets called
    externfunc = random.choice(ExternalFunctions)
    ExternalFunctions.remove(externfunc)
    # All of the others ("noise" functions)
    unusedfuncs = ExternalFunctions

    code = "\tif n <= 1:\n\t\treturn\n"
    didflat, didrec = False, False
    answer = sympy.sympify(0)
    lineswritten = 0

    if for_loop_count:
        co, ans, flat, rec = gen_for(
            funcname=funcname,
            externfunc=externfunc,
            unusedfunc=unusedfuncs,
            current_loop=1,
            num_loops=for_loop_count,
            for_input_opts=forOpts,
            limit=lines_inside_for_loops,
            no_recursion=no_recursion,
        )
        code += co
        answer += ans
        flat = didflat or flat
        rec = didrec or rec
        lineswritten += lines_inside_for_loops

    # didflat ensures at least one call to the function in question
    if not didflat:
        co, ans, _, _ = gen_line(
            funcname=funcname,
            externfunc=externfunc,
            unusedfunc=unusedfuncs,
            force_flat=True,
            no_recursion=no_recursion,
        )
        code += co
        answer += ans
        lineswritten += 1
    # didrec ensures at least one recursive call
    if not didrec and not no_recursion:
        co, ans, _, _ = gen_line(
            funcname=funcname,
            externfunc=externfunc,
            unusedfunc=unusedfuncs,
            force_rec=True,
            no_recursion=no_recursion,
        )
        code += co
        answer += ans
        lineswritten += 1

    # Generate Code outside for loop

    while lineswritten < lines_of_code:
        co, ans, _, _ = gen_line(
            funcname=funcname,
            externfunc=externfunc,
            unusedfunc=unusedfuncs,
            no_recursion=no_recursion,
        )
        code += co
        answer += ans
        lineswritten += 1

    # Calculate the correct answer with sympy formatting
    answer = sympy.sympify(answer)
    bigo = answer
    bigo = bigo.replace(lambda a: a.has(T), lambda a: 0)
    # https://stackoverflow.com/questions/65417468/is-there-a-way-to-strip-an-expression-of-all-functions-of-a-variable-in-sympy
    notbigo = answer - bigo
    ofunc = O(1)
    # This relies on the big O being either 1, polynomial, or a polynomial multiplied by log
    # This block is for O(log(n)), O(nlog(n)), etc.
    if bigo.has(sympy.log(n)):
        nolog = bigo.replace(lambda a: a.has(sympy.log(n)), lambda a: 1)
        nologdeg = sympy.degree(nolog)
        if bigo.has(
            n ** (nologdeg) * sympy.log(n)
        ):  # The log only matters if its attached to the highest degree
            ofunc = O(((1) if nologdeg == 0 else (n**nologdeg)) * sympy.log(n))
        else:
            ofunc = n ** (nologdeg)
    # This block is for no logs, just polynomial inputs
    else:
        odeg = sympy.degree(bigo)
        ofunc = O(1) if odeg == 0 else O(n**odeg)
    finalanswer = notbigo + ofunc

    data["correct_answers"]["custom_function_2"] = pl.to_json(finalanswer)
    renderdict = {
        "code": code,
        "funcname": funcname,
        "externfunc": externfunc,
    }
    #  mypy didn't like the chevron call using QuestionData type.

    with open(
        data["options"]["server_files_course_path"]
        + "/theorielearn/recurrence_equations/recurrence_template.html"
    ) as f:
        data["params"]["html"] = chevron.render(f, renderdict).strip()
