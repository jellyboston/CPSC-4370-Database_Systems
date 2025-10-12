from functional_dependency_set import FunctionalDependency, FunctionalDependencySet
from utils import compute_closure


def determine_redundant_dependencies(
    F: FunctionalDependencySet,
) -> FunctionalDependencySet:
    """
    Determine the redundant dependencies in F

    Postconditions: 
    - Removes a->b from F to computes F' = F \ {a->b}
    - Checks if b subset a+ under F' --> if so, determines redundant FD a->b
    """
    # TODO: implement this function (~ 6 lines)
    redund_fd_set = FunctionalDependencySet()
    F_copy = FunctionalDependencySet(F) # avoids mutability on original
    for fd in F:
        # 1. Compute F'
        F_prm = F_copy.remove_fd(fd)
        # 2. Check if b subset a+ under F'
        a, b = fd
        a_closure = compute_closure(F_prm, a)
        if b.issubset(a_closure):
            # FD a->b is not redundant, so add to unique set
            redund_fd_set.add(FunctionalDependency(a, b))
    return redund_fd_set
