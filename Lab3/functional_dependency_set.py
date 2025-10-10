"""
Contains classes to represent functional dependencies and sets of functional
dependencies.
"""
from typing import List, Set, Union


class FunctionalDependency:
    def __init__(self, alpha: Union[str, Set[str]], beta: Union[str, Set[str]]):
        # convert strings to sets to prevent duplicate attributes
        if isinstance(alpha, str):
            alpha = set(alpha)
        if isinstance(beta, str):
            beta = set(beta)

        self.alpha = alpha
        self.beta = beta

    def __str__(self):
        alpha = "".join(sorted(self.alpha))
        beta = "".join(sorted(self.beta))

        return f"{alpha} -> {beta}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.alpha == other.alpha and self.beta == other.beta

    def __iter__(self):
        return iter((self.alpha, self.beta))

    def __hash__(self) -> int:
        alpha_tuple = tuple(sorted(self.alpha))
        beta_tuple = tuple(sorted(self.beta))

        return hash((alpha_tuple, beta_tuple))

    


class FunctionalDependencySet:
    def __init__(
        self, F: Union[Set[FunctionalDependency], List[FunctionalDependency]] = []
    ):
        self.F = set(F)

    def __str__(self):
        return "\n".join([str(fd) for fd in self.F])

    def __eq__(self, other):
        return self.F == other.F

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        for fd in self.F:
            yield fd

    def add(self, new_fd: FunctionalDependency):
        """
        Add a new functional dependency to the set
        """
        self.F.add(new_fd)

    def remove_fd(self, fd: FunctionalDependency):
        """
        Return the functional dependency set with the given functional
        dependency removed
        """
        if fd not in self.F:
            raise ValueError(f"{fd} not in {self.F}")

        return FunctionalDependencySet([f for f in self.F if f != fd])
