import theorielearn.regular_transformations.server_base as server_base
from theorielearn.shared_utils import QuestionData


def generate(data: QuestionData) -> None:
    data["params"]["language_description"] = r"""
        $PPPREFIX(L) = \{x \mid x \text{ is a proper-proper prefix of some string } w \in L\}.$
        Or alternatively,
        $PPPREFIX(L) = \{ x \mid xy \in L ~\text{for some}~ y\in\Sigma^* ~\text{such that}~ |y|\ge 2 \}.$
        """

    data["params"][
        "commentary"
    ] = r"""Given a string $w$, a prefix is any string $x$ such that there is a string $y$ such
        that $xy=w$. A proper prefix of $w$ is a string $x$ such that there is a $y$ with
        $|y| \geq 1$ such that $xy=w$. We will call a string $x$ a proper-proper prefix
        of $w$ if there is a string y such that $|y| \geq 2$ and $xy = w$. For example, if
        $w = abcde$, then $abc, ab, a,$ and $\epsilon$ are proper-proper prefixes of $w$.
        """
    server_base.generate(data)
