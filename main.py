from core_inst_gen import bound_gap

# Specify the input dimensions
n = 4
m = 3

# Specify the error
epsilon = 0.1

# Specify the number of instances you want to have with high gaps
stored_instance = 30

# Solve
g = bound_gap(n, m, epsilon, stored_instance)
g.core_instance_generator()

# Get results
g.print_results()
