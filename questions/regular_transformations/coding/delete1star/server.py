import theorielearn.regular_transformations.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$L' = \{xy \mid x \cdot 1^n \cdot y \in L ~\text{for some}~ n \ge 0\}$"
    )

    server_base.generate(data)
