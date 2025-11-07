import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$L = \{0^{F_n} \mid n \ge 1\}$, "
        r"where $F_n$ is the $n^\\text{th}$ Fibonacci number (so $F_1 = 1, F_2, = 2, F_3 = 3, F_4 = 5$, etc.)"
    )
    server_base.generate(data)
