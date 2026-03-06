import numpy as np
from itertools import combinations
from pyscipopt import Model
from utils import TOL
from instance import InstanceRestrictedAssignment
from fractions import Fraction
from pyscipopt import Model
from utils import find_covering

# # Instance 1
# p = [9, 9, 7, 3, 9, 8, 3, 2, 6, 5]
# T = 31 # Optimal makespan
# y_non_zero = {(0, (0, 1, 2, 8))  :  5/21, (0, (0, 1, 5, 9))  :  1/3, (0, (0, 2, 3, 4, 6))  :  4/21, (0, (1, 2, 3, 6, 7, 9))  :  1/7, (0, (2, 5, 6, 7, 8, 9))  :  2/21, (1, (1, 2, 4, 9))  :  5/21, (1, (0, 2, 3, 5, 7))  :  2/21, (1, (0, 4, 7, 8, 9))  :  2/21, (1, (0, 3, 6, 7, 8, 9))  :  1/21, (1, (1, 3, 6, 7, 8, 9))  :  1/21, (1, (3, 4, 5, 6, 7, 8))  :  10/21}
# j1 = 0
# j2 = 1
# u_feas = 1
# v_feas = [1, 1, 0, 0, 0 , 0, 0, 0, 0, 0]
# -------------------------------------------------------------------------

# # Instance 2
# p = [30, 46, 81, 30, 55, 71, 33, 22, 5, 93]
# T = 233
# y_non_zero = {
#     (0, (0, 4, 6, 7, 9)) : 1/2, (0, (1, 2, 3, 5, 8)) : 1/2, (1, (0, 1, 2, 5, 8)) : 1/2, (1, (3, 4, 6, 7, 9)) : 1/2
# }
# j1 = 0
# j2 = 4
# u_feas = 6
# v_feas = [1, 1, 2, 1, 2, 2, 1, 0, 0, 2]
# C_max = (0, 1, 2, 5, 8)
# ------------------------------------------------------------------------

# # Instance 5, infeas with option 2, suboptimal with option 1
# p = [2, 2, 2, 1]
# T = 4
# y_non_zero = {
# (0, (0, 3)) : 1/2, (0, (1, 2)) : 1/2, (1, (0, 1)) : 1/2, (1, (2, 3)) : 1/2,
# }
# ass = [1, 0, 1, 0]
# j1 = 0
# j2 = 4
# u_feas = 1
# v_feas = [0.5, 0.5, 0.5, 0.5]
# ------------------------------------------------------------------------

# # Instance 3
# p = [23, 48, 20, 9, 19, 21, 21, 46, 17, 43, 42, 17, 3]
# T = 165
# y_non_zero = {(0, (1, 3, 6, 9, 10)) : 1/4, (0, (1, 3, 7, 9, 11)) : 1/28, (0, (0, 4, 5, 9, 10, 11)) : 1/28, (0, (1, 3, 7, 8, 10, 12)) : 1/4, (0, (2, 4, 5, 7, 8, 10)) : 1/14, (0, (2, 4, 6, 7, 10, 11)) : 1/28, (0, (1, 3, 5, 6, 7, 11, 12)) : 1/28, (0, (2, 4, 5, 9, 10, 11, 12)) : 5/28, (0, (0, 2, 5, 6, 8, 9, 11, 12)) : 3/28, (1, (0, 1, 2, 3, 4, 7)) : 3/7, (1, (5, 6, 7, 8, 9, 11)) : 1/7, (1, (0, 2, 5, 6, 8, 10, 11, 12)) : 5/28, (1, (0, 4, 5, 6, 8, 9, 11, 12)) : 1/4}
# C_max = (0, 1, 3, 9, 10)
# j1 = 0
# j2 = 2
# u_feas = 1
# v_feas = [1, 0, 1] + [0 for _ in range(len(p) - 3)]
# # ------------------------------------------------------------------------

# Instance 4 OK with both methods
p = [12, 59, 56, 8, 16, 25]
T = 89
ass = [1, 1, 0, 0, 1, 0]
y_non_zero = {
    (0, (2, 3, 5)) : 1, (1, (0, 1, 4)) : 1,
}
C_max = (2, 3, 5)
j1 = 0
j2 = 2
u_feas = 1
v_feas = [1, 0, 1, 0, 0, 0]
# # ------------------------------------------------------------------------



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



# Nice, now write the dual
model = Model('Restricted assignment with 2 processing times')


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


#Constrant: u >= 1, This is for getting a new solution with u[0] = 0
# model.addCons(u[0] >= 1, name="u_0_geq_1")

# # Get u', v' -- Tentative 1
# u_prime = 0
# v_prime = []
#
# for j in range(n_jobs):
#     v_prime.append(v_feas[j] - (2*u_feas / n_jobs))
# ---------------------------------------------------------------------------------------------------------------------

# # Get u', v' -- Tentative 2
# u_prime = 0
# v_prime = []
#
# v_non_zeros = [int(v_feas[j] > TOL) for j in range(n_jobs)]
# num_v_non_zeros = sum(v_non_zeros)
#
# for j in range(n_jobs):
#     if v_feas[j] == 0:
#         v_prime.append(0)
#     else:
#         v_prime.append(v_feas[j] - (2 * u_feas / num_v_non_zeros))
# ---------------------------------------------------------------------------------------------------------------------

# # Get u', v' -- Tentative 3
# u_prime = 0
# v_prime = []
#
# # First; find the three configurations that can make a partition --> Set covering
# C_list = find_covering(n_jobs, configs[0])
# C_cover = [set(configs[0][i]) for i in C_list]
#
# for j in range(n_jobs):
#     # Get the set in the cover that contains j
#     C_j = None
#     idx_j = None
#     for idx, C in enumerate(C_cover):
#         if j in C:
#             C_j = C
#             idx_j = idx
#             break
#
#     v_j_prime = (sum(v_feas[i] for i in C_j) - (u_feas)) / len(C_j)
#     v_prime.append(v_j_prime)
# ---------------------------------------------------------------------------------------------------------------------

# Get u', v' -- Tentative 4
u_prime = 0
v_prime = []

# Find the set J1 such that v_feas[j] > 0 for j in J1, and v_feas[j] = 0 for j not in J1
J1 = [j for j in range(n_jobs) if v_feas[j] > TOL]
J2 = [j for j in range(n_jobs) if v_feas[j] <= TOL]

for j in range(n_jobs):
    if j in J1:
        v_j_prime = (sum(v_feas[i] for i in J1) - 2*u_feas) / len(J1)
    else:
        v_j_prime = 0

    v_prime.append(v_j_prime)
# ---------------------------------------------------------------------------------------------------------------------


# Add fake constraint to force the solution to be as I wish
model.addCons(u[0] == u_prime, name="force_u_0")
model.addCons(u[1] == u_prime, name="force_u_1")

for j in range(n_jobs):
    model.addCons(v[j] == v_prime[j], name=f"force_v_{j}")
# -------------------------


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