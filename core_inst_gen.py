"""
Given n (number of jobs), m (number of machines) and an error epsilon,
we wish to enumerate all core instances (m x n matrices with entries of the form k x epsilon)
with the following conditions:

  - The instance encoded by the matrix should have an LP-opt value that is at most 1.
  - In a given matrix, there can be at most 2 different finite entries. The rest of the values are all
    infinite.
  - In each column, all finite values must be the same (<-> machines are identical, apart from infinite values)

We want to enumerate them cleverly (disposing of symmetric or otherwise equivalent cases), as the
number of all such instances is exponential in (n x m) and therefore it's infeasible to handle them
for (n x m) greater than 20. For this, we apply the following (implementation) tricks:

  - TODO
  - TODO
  - TODO

For each instance, we calculate LP-opt and IP-opt. Our upper bound on the empirical gap is
sup{ IP-opt / LP-opt } + (epsilon x n)
"""
from instance import Instance


def core_instance_generator(n, m, epsilon):
    return
