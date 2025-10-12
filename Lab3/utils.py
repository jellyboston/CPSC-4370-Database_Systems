from typing import Set
from functional_dependency_set import FunctionalDependencySet
from functional_dependency_set import FunctionalDependency


def apply_decomposition(F: FunctionalDependencySet) -> FunctionalDependencySet:
    """
    Apply the decomposition property to a set of functional dependencies.

    E.g., if
        F = { A -> CFG }
    this function returns
        F = { A -> C, A -> F, A -> G }

    param F: a set of functional dependencies

    return: a set of functional dependencies with the decomposition property
            applied
    """
    # TODO: implement the decomposition property (~ 4 lines)
    decomposed = FunctionalDependencySet()
    for fd in F:
        lhs, rhs = fd
        for attr in rhs:
            decomposed.add(FunctionalDependency(set(lhs), {attr}))
    return decomposed


def remove_extraneous_attributes(F: FunctionalDependencySet) -> FunctionalDependencySet:
    """
    Remove extraneous attributes on the left hand side from each functional
    dependency in F

    Definition: an attribute is extraneous iff beta is a subset of (alpha - A)^+

    param F: a set of functional dependencies
    return: a set of functional dependencies with extraneous attributes
             removed from the left hand side
    """
    # TODO: implement this function (~ 10 lines)
    output = FunctionalDependencySet()
    for fd in F:
        lhs, rhs = fd # a -> b
        curr_lhs = set(lhs) 
        # test on FDs whose LHS has more than one attribute
        if len(curr_lhs) > 1:
            changed = True
            while changed:
                changed = False
                # iterate over a snapshot since we might mutate current_lhs
                for attr in list(curr_lhs):
                    # only add if not extraneous
                    if rhs.issubset(compute_closure(F, curr_lhs - {attr})):
                        curr_lhs.remove(attr)
                        changed = True
                        break
        output.add(FunctionalDependency(curr_lhs, set(rhs)))
    return output        


def apply_union(F: FunctionalDependencySet) -> FunctionalDependencySet:
    """
    Apply the union property to a set of functional dependencies.

    E.g., if
        F = { A -> C, A -> F, A -> G }
    this function returns
        F = { A -> CFG }

    param F: a set of functional dependencies

    return: a set of functional dependencies with the union property applied
    """
    # TODO: implement the union property (~ 10 lines)
    pass


def compute_closure(F: FunctionalDependencySet, alpha: Set[str]) -> Set[str]:
    """
    Compute the closure of alpha under the set of functional dependencies F

    param F: a set of functional dependencies
    param alpha: a set of attributes

    return: the closure of alpha under F
    """
    # TODO: implement the closure computation (~ 10 lines)
    '''
    Ex for tracing: F1={A→C,A→F,A→G,E→D,AC→D,AD→B,AD→C,CE→B,CF→E,CF→G}
    Find: A+ under F1
    1. Set results = {A}
    2. for every fd, check if lhs is in results
    3. if so, merge rhs to results
    '''
    results = set(alpha)
    changed = True
    while changed:
        # sets are unordered so no index
        changed = False
        for fd in F:
            lhs, rhs = fd
            if lhs.issubset(results):
                # track changes
                before = len(results)
                results |= rhs
                changed = changed or (len(results) > before)
    return results
            

