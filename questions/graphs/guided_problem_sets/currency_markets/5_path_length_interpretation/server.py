import prairielearn as pl
import sympy

def generate(data):

    L = sympy.symbols("L")

    z = 2 ** (-L)

    data["correct_answers"]["q1"] = pl.to_json(z)

def grade(data):
    if(data["score"] != 1):
        data["feedback"]["q1"] = r"Recall that we are taking $\log$ to be base-2."
