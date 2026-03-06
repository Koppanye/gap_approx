TOL = 1e-6
from pyscipopt import Model, quicksum

def find_covering(n, C_list):
    """
    When m = 3, you can cover [n] with three disjoint sets. This function finds those three sets.

    Parameters
    ----------
    n : int
        The number of elements in the universe.
    C_list : list of lists
        The list of configurations (subsets of [n]).

    Returns
    -------
    list of lists
        A list of three lists, each containing the indices of the elements in the corresponding set.
    """
    model = Model("three_disjoint_cover")

    m = len(C_list)

    # decision variables
    x = {}
    for j in range(m):
        x[j] = model.addVar(vtype="B", name=f"x_{j}")

    # exactly three sets
    model.addCons(quicksum(x[j] for j in range(m)) == 3)

    # coverage constraints
    for i in range(n):
        model.addCons(
            quicksum(x[j] for j in range(m) if i in C_list[j]) >= 1
        )

    # disjointness constraints
    for i in range(m):
        for j in range(i + 1, m):
            # If the intersections of C_list[i] and C_list[j] is not empty, then they cannot both be selected
            if set(C_list[i]).intersection(set(C_list[j])):
                model.addCons(x[i] + x[j] <= 1)

    # dummy objective (feasibility problem)
    model.setObjective(0)

    model.optimize()

    if model.getStatus() == "optimal":
        sol = [j for j in range(m) if model.getVal(x[j]) > 0.5]
        return sol
    else:
        return None