import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["commentary"] = (
        r"where XOR(x,y) computes the element-wise XOR of x and y (so for each index i, $z_i = x_i$ XOR $y_i$)."
    )

    data["params"]["language_description"] = (
        r"$L' = \{z \mid z = XOR(x, y) ~\text{for some}~ x \in L ~\text{and}~ y \in L ~\text{such that}~ |x| = |y|\}$"
    )

    server_base.generate(data)
