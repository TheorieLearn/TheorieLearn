import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"$$L = \{ww \mid w \in \Sigma^{\ast}\}$$"

    server_base.generate(data)
