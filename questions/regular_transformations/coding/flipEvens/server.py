import theorielearn.regular_transformations.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$L' = \{\mathit{flipEvens}(w) \mid w \in L\}$"
    )

    data["params"]["commentary"] = (
        r"$\mathit{flipEvens}$ inverts every even-indexed bit in $w$. For example, $\mathit{flipEvens}(01100) = 00110$."
    )

    server_base.generate(data)
