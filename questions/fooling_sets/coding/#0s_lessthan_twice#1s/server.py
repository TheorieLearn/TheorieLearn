import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"Strings over $\{0,1\}$ where the number of 0s is less than twice the number of 1s."
    )

    server_base.generate(data)
