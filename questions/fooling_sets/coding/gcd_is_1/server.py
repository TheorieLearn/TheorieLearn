import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = r"$$L = \{0^m1^n \mid \gcd(m, n) = 1\}$$"

    server_base.generate(data)
