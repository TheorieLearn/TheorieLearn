import theorielearn.CFGs.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$$L = \{w \in \{0,1\}^* \mid \#_0(w) = \#_1(w)\}$$"
    )
    server_base.generate(data)
