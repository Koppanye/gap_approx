from tabnanny import verbose

from instance import InstanceRestrictedAssignment

# Specify the input dimensions
n = 4 # Jobs
m = 3 # Machines

instance = InstanceRestrictedAssignment(n, m, q=0.3)
x, C_max = instance.opt_IP()
C_max_LP_config = instance.opt_LP()