from typing import Set
from functional_dependency_set import FunctionalDependency, FunctionalDependencySet
from utils import (
    apply_decomposition,
    apply_union,
    remove_extraneous_attributes,
)


def compute_minimal_cover(F: FunctionalDependencySet) -> FunctionalDependencySet:
    """
    Compute the minimal cover of F

    param F: a set of functional dependencies
    return: the minimal cover of F
    """
    # 1. TODO: Decompose (1 line)
    decomposed_fds = apply_decomposition(F)

    # 2. TODO: Remove extraneous attributes from the left hand side (1 line)
    unique_fds = remove_extraneous_attributes(decomposed_fds)

    # 3. TODO: Union property (1 line)
    unioned_fds = apply_union(unique_fds)

    return unioned_fds
