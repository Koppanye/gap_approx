from instance import InstanceRestrictedAssignment
from instances_template import pick_one_instance


n, m, M = pick_one_instance("jansen_land_maark_2018_modified")
instance = InstanceRestrictedAssignment(n, m, generate=False, M = M)
sol, C_max = instance.opt_IP()
print(f"Optimal C_max: {C_max}")
C_max_LP = instance.opt_LP(verbose=True)
print(f"Optimal C_max LP relaxation: {C_max_LP}")