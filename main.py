from instance import InstanceRestrictedAssignment

# Specify the input dimensions
n = 4 # Jobs
m = 3 # Machines

instance = InstanceRestrictedAssignment(n, m, q=0.3)
instance.opt_IP()
