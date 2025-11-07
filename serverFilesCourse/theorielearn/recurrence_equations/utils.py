import random

# import prairielearn as pl
import sympy
from sympy import Expr

# creates a for loop.
def gen_for(
    *,
    funcname: str,
    externfunc: str,
    unusedfunc: list[str],
    current_loop: int,
    num_loops: int,
    for_input_opts: dict[str, bool],
    indent: int = 1,
    limit: int = 5,
    force_flat: bool = False,
    no_recursion: bool = False,
) -> tuple[str, Expr, bool, bool]:
    n = sympy.symbols("n")

    itervars = [
        "i",
        "j",
        "k",
        "l",
        "m",
        "a",
        "b",
        "c",
        "d",
        "e",
    ]  # Please don't make a question with this many for loops
    iter = itervars[current_loop - 1]
    # start = 0 if current_loop == 1 else itervars[current_loop - 2]
    # The above doesn't work currently because the way the coefficients of T(n) are determined depends on knowing exactly
    # How many times it loops? I think, I should review recurrences.
    start = 0
    code = ""
    didflat, didrec = False, False
    foranswer = sympy.sympify(0)

    innerfor = 1
    fornfact = random.randint(2, 50)
    jump = random.randint(1, 4)
    ForLoopOpts = [
        f"for ({iter} = {start}; {iter} < n; {iter}++): \n",
        f"for ({iter} = {start}; {iter} < {fornfact}*n; {iter} += {jump}): \n",
        f"for ({iter} = 1; {iter} < n; {iter} *= 2): \n",
        f"for ({iter} = 0; {iter} < {fornfact}; {iter}++): \n",
        f"for ({iter} = 1; {iter} < n**{random.randint(1,3)}; {iter}*={random.randint(2,4)}): \n",
    ]
    Ansops = [n, fornfact * n / jump, sympy.log(n), fornfact, sympy.log(n)]
    ForOptLabels = [
        "n_for_loops",
        "factor_n_for_loops",
        "log_loop",
        "const_for_loops",
        "non_standard_log",
    ]
    forchoices = [
        label[0] for label in enumerate(ForOptLabels) if for_input_opts[label[1]]
    ]

    forloopchosen = random.choice(forchoices)
    code += ("\t" * indent) + ForLoopOpts[forloopchosen]
    innerfor = Ansops[forloopchosen]

    # Generate lines of code or another for loop
    while limit:
        codeline, ansline, flatline, recline = "", sympy.sympify(0), True, True
        if current_loop < num_loops:
            codeline, ansline, flatline, recline = gen_for(
                funcname=funcname,
                externfunc=externfunc,
                unusedfunc=unusedfunc,
                current_loop=current_loop + 1,
                num_loops=num_loops,
                for_input_opts=for_input_opts,
                indent=indent + 1,
                limit=limit,
                force_flat=force_flat,
                no_recursion=no_recursion,
            )
            limit = 1
        else:
            codeline, ansline, flatline, recline = gen_line(
                funcname=funcname,
                externfunc=externfunc,
                unusedfunc=unusedfunc,
                force_flat=force_flat,
                indent=indent + 1,
                no_recursion=no_recursion,
            )
        didflat = flatline or didflat
        didrec = recline or didrec
        code += codeline
        foranswer += (
            innerfor * ansline
        )  # For loops are factored by the number of iterations
        limit -= 1

    foranswer = sympy.sympify(foranswer)
    return code, foranswer, didflat, didrec  # , forlimit


# Creates a single line of code (non for loop)
def gen_line(
    *,
    funcname: str,
    externfunc: str,
    unusedfunc: list[str],
    force_rec: bool = False,
    force_flat: bool = False,
    indent: int = 1,
    no_recursion: bool = False,
) -> tuple[str, Expr, bool, bool]:
    n = sympy.symbols("n")
    T = sympy.Function("T")

    randsub = random.randint(1, 5)
    randdiv = random.randint(2, 4)
    codeops = [
        f"{funcname}(n-{str(randsub)})",
        f"{funcname}(n / {str(randdiv)})",
        f"{random.choice(unusedfunc)}()",
        f"{externfunc}(n)",
    ]
    ansops = [
        T(n - randsub),  # for the func(n-c)
        T(n / randdiv),  # for the func(n/c)
        sympy.sympify(0),  # for the noise function
        sympy.sympify(1),
    ]  # for calling the target function
    # Make the line generated randomly, unless force_rec or force_flat requires a certain type of code.
    # Weighted to encourage more calls to the target function instead of noise or recursive calls.
    index = (
        3
        if force_flat
        else (
            random.randint(2, 3)
            if no_recursion
            else (random.randint(0, 1) if force_rec else min(3, random.randint(0, 5)))
        )
    )

    codestring = ("\t" * indent) + codeops[index] + "\n"
    anseq = ansops[index]
    return codestring, anseq, index == 2, index != 2
