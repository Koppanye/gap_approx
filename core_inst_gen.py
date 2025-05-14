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
from itertools import combinations, combinations_with_replacement, product
import math
import numpy as np


class bound_gap:
    def __init__(self, n, m, epsilon):
        self.n = n
        self.m = m
        self.epsilon = epsilon
        self.largest_num = int(1/self.epsilon)+1  # The largest integer we have to consider
        self.best_gap = None   # We record the highest gap found
        self.gaps = {}         # We also record all gaps for later studies, with multiplicity
        self.gap_bound         # Once finished, it will be self.best_gap + self.n * self.epsilon

    def core_instance_generator(self):
        """
        We generate all possible pairs for 2 processing times (s, b), and call instance_iterator
        to enumerate all of them. Since the gap is invariant to rescaling, we discard all pairs
        whose ratio has been seen before. Due to the lexicographic enumeration,
        it happens iff gcd(s, b) != 1.
        """
        # We treat this case separately, as we have just 1 processing time
        self.instance_iterator(1, 1)

        for (s, b) in combinations(range(1, self.largest_num + 1), 2):
            # We simplify the fraction s/b by finding gcd(s,d)
            if math.gcd(s, b) == 1:
                self.instance_iterator(s, b)
        return True

    def instance_iterator(self, s, b):
        """
        For a given pair (s, b) in {(1, 1), (1, 2), ... , (1/epsilon, 1/epsilon)},
        we generate all inputs up to isomorphism and other redundancies.
        Considerations:
            - If an instance only contains either s or b, then it has already been visited.
              However, we still have to discard all other instances equal-majorating it.
            - If an instance has an LP-optimum larger than 1, then it couldn't have been rounded down
              from an instance with LP-optimum equal to 1.
        """
        visited = {}
        """
        The already visited instances, plus the redundant ones: equivalent up to permutations, 
        or equal-majorate an already seen instance. Whenever we process a new instance, we add
        all its permuted versions, and the ones that equal-majorate it. Before processing a new instance,
        we check whether it is in visited or not. If it is, we pass; if it is not, we process it.
        The instances are stored in an m*n-long string in order to be unhashable.
        """
        for M in combinations_with_replacement(product([0, s, b], repeat=self.n), self.m):
            # We have to check whether M is already found or not.
            if
                # We have to loop through all matrices that majorate M, and
                # all their variants with permuted rows / columns, and add them to visited
                # We switch to numpy for easier handling.
                M = np.array(M)
        return True
