import theorielearn.regular_transformations.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$L' = \{w \mid xwy \in L ~\text{for some}~ x,y \in \Sigma^*\}$"
    )

    server_base.generate(data)
