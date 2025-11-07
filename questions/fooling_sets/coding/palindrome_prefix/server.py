import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"All strings in $\{0, 1\}^{\ast}$ that contain a palindrome of length at least 6 as a prefix."
    )

    server_base.generate(data)
