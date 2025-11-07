import theorielearn.fooling_sets.server_base as server_base


def generate(data):
    data["params"]["language_description"] = (
        r"$$L = \{w \mid \text{the last digit of $|\#(0,w) - \#(1,w)|$ is a 9}\}$$"
    )

    server_base.generate(data)
