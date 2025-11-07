import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"$L = \{0^{\binom{n}{2}} \mid n \ge 0 \}$"

    server_base.generate(data)
