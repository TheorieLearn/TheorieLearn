import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        "All strings where the number of blocks of 0s with even length is the same as the "
        "number of blocks of 0s with odd length. (A block of 0s is a nonempty maximal substring of 0s.)"
    )

    server_base.generate(data)
