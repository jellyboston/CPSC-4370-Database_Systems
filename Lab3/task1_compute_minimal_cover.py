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

    # 2. TODO: Remove extraneous attributes from the left hand side (1 line)

    # 3. TODO: Union property (1 line)

    return F
