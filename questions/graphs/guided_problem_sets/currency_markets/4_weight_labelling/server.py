import prairielearn as pl
import sympy
from prairielearn.sympy_utils import json_to_sympy

def generate(data):

    w = sympy.symbols("w", positive=True)

    z = - sympy.log(w)

    data["correct_answers"]["q1"] = pl.to_json(z)

def grade(data):
    if(data["score"] != 1):

        # default value in case the function doesn't have the free_symbol to take derivative with respect to
        is_strictly_decreasing = False

        expression = json_to_sympy(data["submitted_answers"]["q1"])
        if len(expression.free_symbols) > 0:
            w = list(expression.free_symbols)[0]
            df = sympy.diff(expression, w)
            is_strictly_decreasing = (-1 * df).is_positive

        has_log = expression.has(sympy.log)

        if is_strictly_decreasing and has_log:
            data["feedback"]["q1"] = "It seems like you're using logarithms to convert products to sums, and that your expression is strictly decreasing as $w$ increases, which turns maximization into minimization. Those are both correct approaches! However, is there a simpler expression you could use?"
        elif is_strictly_decreasing:
            data["feedback"]["q1"] = "It seems like your expression is strictly decreasing as $w$ increases, which is a correct approach, as it turns maximization into minimization. However, how can you address the issue that you need to turn a product of ratios into a sum?"
        elif has_log:
            data["feedback"]["q1"] = "You have the correct idea using logarithms to convert products into sums. However, all the relevant graph algorithms minimize sums, but we aim to maximize values. How can you address this?"
        else:
            data["feedback"]["q1"] = "Our problem boils down to trying to maximize the product of ratios, but all the relevant graph algorithms minimize sums. Therefore, we need to do 2 things. First, we need to convert a product into a sum. Is there a function that can help with that? Second, we need to convert maximization into minimization. How can we ensure larger $w$ coorespond to a smaller value of the expression?"
    
       

        

            
        

