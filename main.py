from instance import InstanceRestrictedAssignment
from instances_template import pick_one_instance
import numpy as np


#n, m, M = pick_one_instance("jansen_land_maark_2018_modified")
M = np.array([[3, 6, 12, 24, 17, 33, 66, 132, 264, 528, 160, 640, 576, 320, 288],
              [3, 6, 12, 24, 17, 33, 66, 132, 264, 528, 160, 640, 576, 320, 288],
              [3, 6, 12, 24, 17, 33, 66, 132, 264, 528, 160, 640, 576, 320, 288]
            ])

n = M.shape[1]
m = M.shape[0]
instance = InstanceRestrictedAssignment(n, m, generate=False, M = M)
sol, C_max = instance.opt_IP()
print(f"Optimal C_max: {C_max}")
C_max_LP = instance.opt_LP(verbose=True, C_max=C_max)
print(f"Optimal C_max LP relaxation: {C_max_LP}")