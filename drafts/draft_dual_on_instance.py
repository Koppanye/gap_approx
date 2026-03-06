import numpy as np
from itertools import combinations
from pyscipopt import Model
from utils import TOL
from instance import InstanceRestrictedAssignment
from fractions import Fraction
from pyscipopt import Model, SCIP_RESULT

# # Instance 1
# p = [9, 9, 7, 3, 9, 8, 3, 2, 6, 5]
# T = 31 # Optimal makespan
# y_non_zero = {(0, (0, 1, 2, 8))  :  5/21, (0, (0, 1, 5, 9))  :  1/3, (0, (0, 2, 3, 4, 6))  :  4/21, (0, (1, 2, 3, 6, 7, 9))  :  1/7, (0, (2, 5, 6, 7, 8, 9))  :  2/21, (1, (1, 2, 4, 9))  :  5/21, (1, (0, 2, 3, 5, 7))  :  2/21, (1, (0, 4, 7, 8, 9))  :  2/21, (1, (0, 3, 6, 7, 8, 9))  :  1/21, (1, (1, 3, 6, 7, 8, 9))  :  1/21, (1, (3, 4, 5, 6, 7, 8))  :  10/21}


# Instance 2
p = [30, 46, 81, 30, 55, 71, 33, 22, 5, 93]
T = 233
y_non_zero = {
    (0, (0, 4, 6, 7, 9)) : 1/2, (0, (1, 2, 3, 5, 8)) : 1/2, (1, (0, 1, 2, 5, 8)) : 1/2, (1, (3, 4, 6, 7, 9)) : 1/2
}

# # Instance 3
# p = [23, 48, 20, 9, 19, 21, 21, 46, 17, 43, 42, 17, 3]
# T = 165
# y_non_zero = {(0, (1, 3, 6, 9, 10)) : 1/4, (0, (1, 3, 7, 9, 11)) : 1/28, (0, (0, 4, 5, 9, 10, 11)) : 1/28, (0, (1, 3, 7, 8, 10, 12)) : 1/4, (0, (2, 4, 5, 7, 8, 10)) : 1/14, (0, (2, 4, 6, 7, 10, 11)) : 1/28, (0, (1, 3, 5, 6, 7, 11, 12)) : 1/28, (0, (2, 4, 5, 9, 10, 11, 12)) : 5/28, (0, (0, 2, 5, 6, 8, 9, 11, 12)) : 3/28, (1, (0, 1, 2, 3, 4, 7)) : 3/7, (1, (5, 6, 7, 8, 9, 11)) : 1/7, (1, (0, 2, 5, 6, 8, 10, 11, 12)) : 5/28, (1, (0, 4, 5, 6, 8, 9, 11, 12)) : 1/4}
#

# # Instance 4 OK with both methods
# p = [12, 59, 56, 8, 16, 25]
# T = 89
# ass = [1, 1, 0, 0, 1, 0]
# y_non_zero = {
#     (0, (2, 3, 5)) : 1, (1, (0, 1, 4)) : 1,
# }

# # Instance 5, infeas with option 2, suboptimal with option 1
# p = [2, 2, 2, 1]
# T = 4
# y_non_zero = {
# (0, (0, 3)) : 1/2, (0, (1, 2)) : 1/2, (1, (0, 1)) : 1/2, (1, (2, 3)) : 1/2,
# }
# ass = [1, 0, 1, 0]

# For everything
n_jobs = len(p)
n_machines = 2
M = np.asarray([p for _ in range(n_machines)])


# Random
# n_jobs = 13
# n_machines = 2
# p = [np.random.randint(1, 50) for _ in range(n_jobs)]



# #-----------------------
# # If you need to solve the IP
# print(f"p = {p}", flush=True)
# instance = InstanceRestrictedAssignment(n_jobs, n_machines, generate=False, M = M)
# print("Instance generated!", flush=True)
# ass, T_int = instance.opt_IP(verbose=True)
#
# #-----------------------
# # # If you need to solve the LP
# instance = InstanceRestrictedAssignment(n_jobs, n_machines, generate=False, M = M)
# print("Instance generated!", flush=True)
# LP, y = instance.opt_LP(verbose=True)
# for k in y.keys():
#     if y[k] > TOL:
#         print(k, ":", Fraction(y[k]).limit_denominator(), end=", ")
#
# print(f"Optimal makespan {T}")


# Determining valid configurations (with makespan at most T) for each machine in the form of a dict
# Values are lists of tuples, one tuple for each valid configuration
configs = {i: [c for length in range(1, n_jobs + 1) for c in combinations([j for j in range(n_jobs) if M[i][j] != 0], length) if sum(int(M[i][j]) for j in c) <= T] for i in range(n_machines)}

# Create al the combinations of two jobs
#j_pairs = combinations(range(n_jobs), 2)
#for j1, j2 in j_pairs:
j1 = 0
j2 = 1

# Nice, now write the dual
model = Model('Restricted assignment with 2 processing times')

# -------------
# Some parameters
get_more_opt = False
if get_more_opt:
    model.setParam("limits/maxsol", 10)   # allow many stored solutions

# Add variables
u = []
v = []
for i in range(n_machines):
    #u.append(model.addVar(vtype="C", name=f"u({i})", lb=0.0))
    u.append(model.addVar(vtype="C", name=f"u({i})", lb=None))


for j in range(n_jobs):
    #v.append(model.addVar(vtype="C", name=f"v({j})", lb=0.0))
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

# Add a fake constraint
# model.addCons(-sum(u) + sum(v) >= 2*TOL, name="absurdum")


# Try e feasible solution
u_feas = 1

# Option 1
v_feas = []
for j in range(n_jobs):
    configs_j = [C for C in configs[0] if j in C]
    weight_config_j = [sum(p[j] for j in C) for C in configs_j]
    # Pick maximum
    max_weight_config_j = max(weight_config_j)
    v_feas.append(Fraction(u_feas * p[j] / max_weight_config_j).limit_denominator())

# Option 2
# # Forcing solutions
# v_feas = []
# for j in range(n_jobs):
#     v_j_feas_den = 0
#     for i, C in y_non_zero:
#         if j in C:
#             v_j_feas_den += y_non_zero[(i, C)] * sum(p[q] for q in C) * u_feas
#     v_feas.append(Fraction(p[j] / v_j_feas_den).limit_denominator())
#
# # Add fake constraint to force the solution to be as I wish
# model.addCons(u[0] == u_feas, name="force_u")
# model.addCons(u[1] == u_feas, name="force_u_2")
#
# for j in range(n_jobs):
#     model.addCons(v[j] == v_feas[j], name=f"force_v_{j}")
# # -------------------------

# # Option 3
# # Forcing solutions
# v_feas = []
# for j in range(n_jobs):
#     v_j_feas = 0
#     for i, C in y_non_zero:
#         if j in C and j1 in C and j2 in C:
#             v_j_feas += y_non_zero[(i, C)] * u_feas / max([len(C) for C in y_non_zero])
#
#     v_feas.append(v_j_feas)

# Add fake constraint to force the solution to be as I wish
model.addCons(u[0] == u_feas, name="force_u")
model.addCons(u[1] == u_feas, name="force_u_2")

for j in range(n_jobs):
    model.addCons(v[j] == v_feas[j], name=f"force_v_{j}")
# -------------------------


# # Just force u
# u_feas = 1
# model.addCons(u[0] == u_feas, name="force_u")
# model.addCons(u[1] == u_feas, name="force_u_2")
# #----------------------------

model.optimize()

if model.getStatus() == "optimal":
    if get_more_opt:
        sols = model.getSols()
        best_obj = model.getObjVal()

        for i, sol in enumerate(sols):
            if model.getSolObjVal(sol) == best_obj:
                print(f"\nOptimal solution {i + 1}")
                for var in model.getVars():
                    print(var.name, model.getSolVal(sol, var))
    else:
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
        print(f"sum of $v_j$ for j in the config having the max weight: ", sum(v_star[i] for i in max_config))
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

        print(f"sum of $v_j$ for j in the longest configuration:", sum(v_star[i] for i in longest_config))
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

# print("\n→ → → → → → → → → → →")
# # Fix one variable
# j_test = 2
# for C in configs[0]:
#     if j_test in C:
#         this_C = sum(p[j] for j in C)
#         print(f"{p[j_test]} --> {Fraction(this_C * p[j_test] / T).limit_denominator()}")