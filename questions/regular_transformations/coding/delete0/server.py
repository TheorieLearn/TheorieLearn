import theorielearn.regular_transformations.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"$L' = \{xy \mid x0y \in L\}$"

    server_base.generate(data)
