import numpy as np
from instance import InstanceRestrictedAssignment
from utils import TOL
from itertools import combinations
from pyscipopt import Model
from fractions import Fraction
from tqdm import tqdm

def solve_dual_with_u_geq_1(j1, j2):
    model = Model('Restricted assignment with 2 processing times')

    # Silent output
    model.setParam('display/verblevel', 0)

    # Add variables
    u = []
    v = []
    for i in range(n_machines):
        # u.append(model.addVar(vtype="C", name=f"u({i})", lb=0.0))
        u.append(model.addVar(vtype="C", name=f"u({i})", lb=None))

    for j in range(n_jobs):
        # v.append(model.addVar(vtype="C", name=f"v({j})", lb=0.0))
        v.append(model.addVar(vtype="C", name=f"v({j})", lb=None))

    # Objective functuon
    model.setObjective(-sum(u) + sum(v), "maximize")

    for i in range(n_machines):
        for C in configs[i]:
            if j1 in C and j2 in C:
                rhs = 1
            else:
                rhs = 0
            model.addCons(-u[i] + sum(v[j] for j in C) <= rhs, name=f"{i} - {C}")

    # Constrant: u >= 1, This is for getting a new solution with u[0] = 0
    model.addCons(u[0] >= 1, name="u_0_geq_1")

    model.optimize()

    if model.getStatus() == "optimal":
        v_star = {j: Fraction(model.getVal(v[j])).limit_denominator() for j in range(n_jobs)}
        u_star = {i: Fraction(model.getVal(u[i])).limit_denominator() for i in range(n_machines)}
        obj = model.getObjVal()

        if obj <= TOL:
            return v_star, u_star, obj
        else:
            raise ValueError("Non zero solution found, but expected zero.")
    else:
        raise ValueError("No optimal solution found when u >= 1.")


def solve_dual_with_v_prime(u_feas, v_feas):
    model = Model()
    # Silent output
    model.setParam('display/verblevel', 0)

    # Add variables
    u = []
    v = []
    for i in range(n_machines):
        # u.append(model.addVar(vtype="C", name=f"u({i})", lb=0.0))
        u.append(model.addVar(vtype="C", name=f"u({i})", lb=None))

    for j in range(n_jobs):
        # v.append(model.addVar(vtype="C", name=f"v({j})", lb=0.0))
        v.append(model.addVar(vtype="C", name=f"v({j})", lb=None))

    # Objective functuon
    model.setObjective(-sum(u) + sum(v), "maximize")

    for i in range(n_machines):
        for C in configs[i]:
            if j1 in C and j2 in C:
                rhs = 1
            else:
                rhs = 0
            model.addCons(-u[i] + sum(v[j] for j in C) <= rhs, name=f"{i} - {C}")

    u_prime = 0
    v_prime = []

    # Find the set J1 such that v_feas[j] > 0 for j in J1, and v_feas[j] = 0 for j not in J1
    J1 = [j for j in range(n_jobs) if v_feas[j] > TOL]

    for j in range(n_jobs):
        if j in J1:
            v_j_prime = (sum(v_feas[i] for i in J1) - 2 * u_feas) / len(J1)
        else:
            v_j_prime = 0

        v_prime.append(v_j_prime)

    # Add fake constraint to force the solution to be as I wish
    model.addCons(u[0] == u_prime, name="force_u_0")
    model.addCons(u[1] == u_prime, name="force_u_1")

    for j in range(n_jobs):
        model.addCons(v[j] == v_prime[j], name=f"force_v_{j}")

    model.optimize()

    if model.getStatus() == "optimal":
        v_star = {j: Fraction(model.getVal(v[j])).limit_denominator() for j in range(n_jobs)}
        u_star = {i: Fraction(model.getVal(u[i])).limit_denominator() for i in range(n_machines)}
        obj = model.getObjVal()

        if obj <= TOL:
            return v_star, u_star, obj
        else:
            raise ValueError("Non zero solution found, but expected zero.")
    else:
        raise ValueError("No optimal solution found when u' = 0, and v' as described.")

if __name__ == "__main__":
    m = 2

    # Generate n
    seed_min = 0
    seed_max = 1000

    n_machines = 2
    for seed in tqdm(range(seed_min, seed_max)):
        np.random.seed(seed)

        n_jobs = np.random.randint(4, 13)

        p = np.random.randint(1, 100, (n_jobs,))

        # Get M
        M = np.asarray([p for _ in range(n_machines)])

        # Solve the LP
        instance = InstanceRestrictedAssignment(n_jobs, n_machines, generate=False, M=M)
        T, y = instance.opt_LP(verbose=False)

        y_non_zero = {k : y[k] for k in y if y[k] > TOL}


        configs = {i: [c for length in range(1, n_jobs + 1) for c in
                       combinations([j for j in range(n_jobs) if M[i][j] != 0], length) if
                       sum(int(M[i][j]) for j in c) <= T] for i in range(n_machines)}

        max_config_weight = 0
        max_config = None
        for C in configs[0]:
            config_weight = sum(p[j] for j in C)
            if config_weight > max_config_weight:
                max_config_weight = config_weight
                max_config = C


        j1 = max_config[0]
        j2 = min([j for j in range(n_jobs) if j not in max_config])

        v_feas, u_feas, obj = solve_dual_with_u_geq_1(j1, j2)

        u_feas = u_feas[0]
        v_feas = [v_feas[j] for j in range(n_jobs)]

        v_prime, u_prime, obj_prime = solve_dual_with_v_prime(u_feas, v_feas)