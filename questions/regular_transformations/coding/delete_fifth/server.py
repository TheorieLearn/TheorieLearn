import theorielearn.regular_transformations.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$L' = \{xy \mid xay \in L ~\text{for some}~x,y \in \Sigma^* ~\text{and}~ a \in \Sigma ~\text{such that}~ |y| = 4\}$"
    )

    server_base.generate(data)
