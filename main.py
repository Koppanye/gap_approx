from instance import InstanceRestrictedAssignment
from instances_template import pick_one_instance
import numpy as np


#n, m, M = pick_one_instance("jansen_land_maark_2018_modified")
M = np.array([[-1, 13, -1, -1, -1, -1, 80, 65, -1, -1, 77, 72,  7, 26, -1, -1,
        -1, -1, 12, -1, -1, 15, -1, 69, 88, 88, 95, -1, 87, 14, -1, -1,
        -1, -1, 23, -1, -1, -1, 61, -1, -1, 89, 14, -1, 73, -1, -1,  4,
        71, 22, 50, 58,  4, -1, 25, 44, 77, -1, -1, -1, 42, 83, 16, -1,
        69, -1, -1, 88,  8, 27, 26, 23, -1, -1, -1, -1, 38, 58, 84, 39,
         9, 33, 35, -1, -1, 16, 88, 26, 72, -1, -1, -1, 47, -1, 89, 24,
        -1, 66, -1,  4],
       [38, -1, 73, 10, 76,  6, -1, -1, 17,  2, -1, -1, -1, -1, 51, 21,
        19, 85, -1, 29, 30, -1, 51, -1, -1, -1, -1, 97, -1, -1, 10,  8,
        64, 62, -1, 58,  2,  1, -1, 82,  9, -1, -1, 48, -1, 31, 72, -1,
        -1, -1, -1, -1, -1, 69, -1, -1, -1, 27, 53, 81, -1, -1, -1, 65,
        -1, 26, 99, -1, -1, -1, -1, -1, 10, 68, 24, 28, -1, -1, -1, -1,
        -1, -1, -1, 11, 24, -1, -1, -1, -1, 93, 75, 63, -1, 33, -1, -1,
        56, -1, 78, -1]])
# Replace -1 with 0
M[M == -1] = 0 # m x n
n = M.shape[1]
m = M.shape[0]
instance = InstanceRestrictedAssignment(n, m, generate=False, M = M)
sol, C_max = instance.opt_IP()
print(f"Optimal C_max: {C_max}")
C_max_LP = instance.opt_LP(verbose=True, C_max=C_max)
print(f"Optimal C_max LP relaxation: {C_max_LP}")