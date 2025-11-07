import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$$L = \{w \mid w \\text{ is a palindrome}\}$$"
    )

    server_base.generate(data)
