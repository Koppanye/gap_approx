import numpy as np
from itertools import combinations
from pyscipopt import Model
from utils import TOL
from instance import InstanceRestrictedAssignment
from fractions import Fraction

#p = [9, 9, 7, 3, 9, 8, 3, 2, 6, 5]
#T = 31 # Optimal makespan
# n_jobs = len(p)

n_jobs = 13
p = [np.random.randint(1, 100) for _ in range(n_jobs)]
n_jobs = len(p)
#p = [np.random.randint(1, 10) for _ in range(n_jobs)]
print(f"p = {p}", flush=True)
n_machines = 2
M = np.asarray([p for _ in p])

instance = InstanceRestrictedAssignment(n_jobs, n_machines, generate=False, M = M)
print("Instance generated!", flush=True)
T, x = instance.opt_LP(verbose=True)
print(f"Optimal makespan {T}")


# Determining valid configurations (with makespan at most T) for each machine in the form of a dict
# Values are lists of tuples, one tuple for each valid configuration
configs = {i: [c for length in range(1, n_jobs + 1) for c in combinations([j for j in range(n_jobs) if M[i][j] != 0], length) if sum(int(M[i][j]) for j in c) <= T] for i in range(n_machines)}

# Create al the combinations of two jobs
j_pairs = combinations(range(n_jobs), 2)

for j1, j2 in j_pairs:
    # Nice, now write the dual
    model = Model('Restricted assignment with 2 processing times')
    model.hideOutput()

    # Add variables
    u = []
    v = []
    for i in range(n_machines):
        u.append(model.addVar(vtype="C", name=f"u({i})", lb=0.0))

    for j in range(n_jobs):
        v.append(model.addVar(vtype="C", name=f"v({j})", lb=0.0))

    # Objective functuon
    model.setObjective(-sum(u) + sum(v), "maximize")

    for i in range(n_machines):
        for C in configs[i]:
            if j1 in C and j2 in C:
                rhs = 1
            else:
                rhs = 0
            model.addCons(-u[i] + sum(v[j] for j in C) <= rhs)

    # Add a fake constraint
    model.addCons(u[0] >= 1)

    model.optimize()

    obj = model.getObjVal()

    if obj <= TOL:
        print(f"j1 = {j1} and j2 = {j2}")
        print(f"Objetive value = {obj}")
        for i in range(n_machines):
            u_i = model.getVal(u[i])
            if u_i >= TOL:
                print(f"u[{i}] = {u_i}")
        for j in range(n_jobs):
            v_j = model.getVal(v[j])
            if v_j >= TOL:
                print(f"v[{j}] = {Fraction(v_j).limit_denominator()}")

        print("→ → → → → → → → → → →")
        _ = input("Continue?")
