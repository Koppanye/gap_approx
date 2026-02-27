import numpy as np
from itertools import combinations
from pyscipopt import Model
from utils import TOL
from instance import InstanceRestrictedAssignment
from fractions import Fraction
from pyscipopt import Model, SCIP_RESULT

# # Instance 1
#p = [9, 9, 7, 3, 9, 8, 3, 2, 6, 5]
# T = 31 # Optimal makespan

# # Instance 2
# p = [30, 46, 81, 30, 55, 71, 33, 22, 5, 93]
# T = 233
# Constraint: 1 - (0, 1, 2, 5, 8)
# Constraint: 0 - (3, 4, 6, 7, 9)

# # Instance 3
# p = [23, 48, 20, 9, 19, 21, 21, 46, 17, 43, 42, 17, 3]
# T = 165

# Instance 4
p = [12, 59, 56, 8, 16, 25]
T = 89
ass = [1, 1, 0, 0, 1, 0]


# For everything
n_jobs = len(p)
n_machines = 2
M = np.asarray([p for _ in range(n_machines)])


# Random
# n_jobs = 13
# n_machines = 2
# p = [np.random.randint(1, 50) for _ in range(n_jobs)]

# -----------------------
# # If you need to solve the IP
# print(f"p = {p}", flush=True)
# instance = InstanceRestrictedAssignment(n_jobs, n_machines, generate=False, M = M)
# print("Instance generated!", flush=True)
# ass, T_int = instance.opt_IP(verbose=True)

print(f"Optimal makespan {T}")


# Determining valid configurations (with makespan at most T) for each machine in the form of a dict
# Values are lists of tuples, one tuple for each valid configuration
configs = {i: [c for length in range(1, n_jobs + 1) for c in combinations([j for j in range(n_jobs) if M[i][j] != 0], length) if sum(int(M[i][j]) for j in c) <= T] for i in range(n_machines)}

# Create al the combinations of two jobs
#j_pairs = combinations(range(n_jobs), 2)
#for j1, j2 in j_pairs:
j1 = 4
j2 = 5

# Nice, now write the dual
model = Model('Restricted assignment with 2 processing times')

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
        model.addCons(-u[i] + sum(v[j] for j in C) <= rhs, name=f"{i} - {C}")

# Add a fake constraint
# model.addCons(-sum(u) + sum(v) >= 2*TOL, name="absurdum")

# Add >= 1 constraint for u0
model.addCons(u[0] >= 1, name="u0_geq_1")

model.optimize()

if model.getStatus() == "optimal":
    v_star = {j : Fraction(model.getVal(v[j])).limit_denominator() for j in range(n_jobs)}
    u_star = {i : Fraction(model.getVal(u[i])).limit_denominator() for i in range(n_machines)}
    obj = model.getObjVal()

    max_config_weight = 0
    max_config = None
    for C in configs[0]:
        config_weight = sum(p[j] for j in C)
        if config_weight > max_config_weight:
            max_config_weight = config_weight
            max_config = C

    print("Configuration with max weight", max_config, "with weight", max_config_weight)
    print("v in the config having the max weight", sum(v_star[i] for i in max_config))
    for i in max_config:
        print(f"v[{i}] = {v_star[i]}, p[{i}] = {p[i]}; ", end=" ")
    print("\n→ → → → → → → → → → →")

    # Longest configuration
    length_longest_config = 0
    longest_config = None
    for C in configs[0]:
        if len(C) > length_longest_config:
            length_longest_config = len(C)
            longest_config = C

    print("v in the config having longest value", sum(v_star[i] for i in longest_config))
    for i in longest_config:
        print(f"v[{i}] = {v_star[i]}, p[{i}] = {p[i]}; ", end=" ")
    print("\n→ → → → → → → → → → →")


    for i in range(n_jobs):
        print(f"v[{i}] = {Fraction(v_star[i]).limit_denominator()}")
    for j in range(n_machines):
        print(f"u[{j}] = {Fraction(u_star[j]).limit_denominator()}")
    print("→ → → → → → → → → → →")
else:
    # Write the model
    iis = model.generateIIS()

    subscip = iis.getSubscip()  # Get constraints in the IISfor cons in subscip.getConss():
    for cons in subscip.getConss():
        print(f"Constraint: {cons.name}")  # Get variables in the IISfor var in subscip.getVars():

print("\n→ → → → → → → → → → →")
# Fix one variable
j_test = 2
for C in configs[0]:
    if j_test in C:
        this_C = sum(p[j] for j in C)
        print(f"{p[j_test]} --> {Fraction(this_C * p[j_test] / T).limit_denominator()}")