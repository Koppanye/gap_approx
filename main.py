from core_inst_gen import bound_gap

# Specify the input dimensions
n = 3
m = 4

# Specify the error
epsilon = 0.01

# Specify the number of instances you want to have with high gaps
stored_instance = 30

# Solve
g = bound_gap(n, m, epsilon, stored_instance)

# Get results
g.print_results()
