import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        "All strings where the subsequence 01 appears the same number of times as the subsequence 10."
    )

    server_base.generate(data)
